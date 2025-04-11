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
        fieldnames = ['user', 'salary', 'debt', 'savings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write headers only if the file does not exist
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data)

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
        
        # Store in variables
        financial_data = {
            'user': user_number,
            'salary': salary,
            'debt': debt,
            'savings': savings
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
        
        # Use the financial data
        plan_run = portia.run(f'Analyze financial data: Salary {salary}, Debt {debt}, Savings {savings}')
        final_output_value = plan_run.outputs.final_output.value
        
        # Append output to file
        with open("output.txt", "a") as f:
            f.write(f"User {user_number} analysis:\n{final_output_value}\n\n")
        
        return f"""
            <div style="font-family: Arial; max-width: 500px; margin: 0 auto;">
                <h2>Data received for User {user_number}!</h2>
                <p><strong>Salary:</strong> {salary}</p>
                <p><strong>Debt:</strong> {debt}</p>
                <p><strong>Savings:</strong> {savings}</p>
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
