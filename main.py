from flask import Flask, request, render_template, send_from_directory
import os
import csv
from dotenv import load_dotenv
from portia import (
    Config,
    LLMModel,
    LLMProvider,
    Portia,
    example_tool_registry,
)

app = Flask(__name__, template_folder='frontend', static_folder='frontend')

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Function to get the next user number
def get_next_user_number():
    try:
        with open("user_counter.txt", "r") as f:
            return int(f.read().strip()) + 1
    except FileNotFoundError:
        return 1

# Function to save the current user number
def save_user_number(number):
    with open("user_counter.txt", "w") as f:
        f.write(str(number))

# Function to save data to CSV
def save_to_csv(data):
    file_exists = os.path.isfile("financial_data.csv")
    
    with open("financial_data.csv", "a", newline="") as csvfile:
        fieldnames = ['user', 'salary', 'debt', 'savings', 'credit_score']  # Add 'credit_score'
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write headers only if the file does not exist
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data)

# Function to calculate estimated credit score
def estimate_credit_score(salary, savings, debt):
    # Calculate Debt-to-Income (DTI) ratio
    dti = debt / salary if salary != 0 else 0

    # Calculate Savings-to-Income ratio
    savings_to_income = savings / salary if salary != 0 else 0

    # Base score for average individuals
    base_score = 650

    # Modify score based on DTI
    if dti > 0.4:
        base_score -= 100  # High debt-to-income ratio decreases score
    elif dti > 0.2:
        base_score -= 50  # Moderate DTI decrease

    # Modify score based on Savings-to-Income
    if savings_to_income > 0.2:
        base_score += 50  # High savings increases score
    elif savings_to_income > 0.1:
        base_score += 25  # Moderate savings increases score

    # Ensure the score stays within a reasonable range (300 to 850)
    estimated_score = max(300, min(base_score, 850))

    return estimated_score

# Function to read data from CSV and prepare the query
def read_and_prepare_csv_query():
    query_list = []

    # Read the financial data from the CSV
    with open("financial_data.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            salary = row['salary']
            debt = row['debt']
            savings = row['savings']
            # Prepare the query for Gemini
            query = f"Analyze financial data: Salary: £{salary}, Debt: £{debt}, Savings: £{savings}."
            query_list.append(query)
    
    return query_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get form data
        salary = request.form.get('salary', '')
        debt = request.form.get('debt', '')
        savings = request.form.get('savings', '')
        
        if not all([salary, debt, savings]):
            return "Please fill all fields", 400
            
        # Get and increment user number
        user_number = get_next_user_number()
        save_user_number(user_number)
        
        # Convert input values to floats
        salary = float(salary)
        debt = float(debt)
        savings = float(savings)
        
        # Estimate the credit score
        credit_score = estimate_credit_score(salary, savings, debt)
        
        # Store in variables
        financial_data = {
            'user': user_number,
            'salary': salary,
            'debt': debt,
            'savings': savings,
            'credit_score': credit_score  # Add credit score to data
        }
        
        # Save data to CSV
        save_to_csv(financial_data)
        
        # Initialize Portia
        google_config = Config.from_default(
            llm_provider=LLMProvider.GOOGLE_GENERATIVE_AI,
            llm_model_name=LLMModel.GEMINI_2_0_FLASH,
            google_api_key=GOOGLE_API_KEY
        )
        portia = Portia(config=google_config, tools=example_tool_registry)
        
        # Read and prepare the query for Gemini from the CSV data
        queries = read_and_prepare_csv_query()

        # Send each query to Portia (Gemini model)
        analysis_results = []
        for query in queries:
            plan_run = portia.run(query)
            final_output_value = plan_run.outputs.final_output.value
            analysis_results.append(final_output_value)

        # Store analysis in output.txt
        with open("output.txt", "a") as f:
            for i, result in enumerate(analysis_results):
                f.write(f"User {i + 1} analysis:\n{result}\n\n")

        return f"""
            <div style="font-family: Arial; max-width: 500px; margin: 0 auto;">
                <h2>Data received for User {user_number}!</h2>
                <p><strong>Salary:</strong> {salary}</p>
                <p><strong>Debt:</strong> {debt}</p>
                <p><strong>Savings:</strong> {savings}</p>
                <p><strong>Estimated Credit Score:</strong> {credit_score}</p>
                <p>Results appended to files.</p>
                <a href="/" style="display: inline-block; margin-top: 20px; padding: 10px; background: #4CAF50; color: white; text-decoration: none;">Submit Another</a>
            </div>
        """
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)
