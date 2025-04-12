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

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='frontend', static_folder='frontend')

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# User ID counter
def get_next_user_number():
    try:
        with open("user_counter.txt", "r") as f:
            return int(f.read().strip()) + 1
    except FileNotFoundError:
        return 1

def save_user_number(number):
    with open("user_counter.txt", "w") as f:
        f.write(str(number))

# Save to CSV
def save_to_csv(data):
    file_exists = os.path.isfile("financial_data.csv")
    with open("financial_data.csv", "a", newline="") as csvfile:
        fieldnames = ['user', 'salary', 'debt', 'savings', 'dti', 'savings_rate', 'net_worth']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def calculate_financial_metrics(salary, debt, savings):
    """Calculate all financial metrics locally"""
    dti = round((debt/salary)*100, 2) if salary else 0
    savings_rate = round((savings/salary)*100, 2) if salary else 0
    net_worth = savings - debt
    return dti, savings_rate, net_worth

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        salary = float(request.form.get('salary', ''))
        debt = float(request.form.get('debt', ''))
        savings = float(request.form.get('savings', ''))
        model_choice = request.form.get('model', 'gemini').lower()

        if not all([salary, debt, savings]):
            return "Please fill all fields", 400

        user_number = get_next_user_number()
        save_user_number(user_number)

        financial_data = {
            'user': user_number,
            'salary': salary,
            'debt': debt,
            'savings': savings,
            'dti': dti,
            'savings_rate': savings_rate,
            'net_worth': net_worth
        }
        save_to_csv(financial_data)

        # AI prompt
        prompt = f"""
        Based on these exact financial numbers:
        Salary=${salary}, Debt=${debt}, Savings=${savings}, DTI={dti}%, SavingsRate={savings_rate}%, NetWorth=${net_worth}

        Calculate their:
        1. Debt-to-Income Ratio (DTI)
        2. Savings Rate
        3. Net Worth

        Then provide a short paragraph interpreting these values and giving practical suggestions to improve their financial situation.
        """

        # Configure Gemini
        config = Config.from_default(
            llm_provider=LLMProvider.GOOGLE_GENERATIVE_AI,
            llm_model_name=LLMModel.GEMINI_2_0_FLASH,
            google_api_key=GOOGLE_API_KEY
        )

        portia = Portia(config=config, tools=[])  # No search tools
        plan_run = portia.run(prompt)
        result = plan_run.outputs.final_output.value

        if isinstance(result, list):
            result = " ".join(result)

        formatted_advice = "<p>" + advice.replace('\n', '</p><p>') + "</p>"

        with open("output.txt", "a") as f:
            f.write(f"User {user_number} analysis:\n{result}\n\n")

        return f"""
            <div style="font-family: Arial; max-width: 500px; margin: 0 auto;">
                <h2>Financial Analysis for User {user_number}</h2>
                <div style="margin-bottom: 20px;">
                    <p><strong>Salary:</strong> ${salary:,.2f}</p>
                    <p><strong>Debt:</strong> ${debt:,.2f}</p>
                    <p><strong>Savings:</strong> ${savings:,.2f}</p>
                </div>
                <div style="margin-bottom: 20px; background-color: #f0f8ff; padding: 10px; border-radius: 5px;">
                    <h3>Calculated Metrics:</h3>
                    <p><strong>Debt-to-Income Ratio:</strong> {dti}%</p>
                    <p><strong>Savings Rate:</strong> {savings_rate}%</p>
                    <p><strong>Net Worth:</strong> ${net_worth:,.2f}</p>
                </div>
                <div style="background-color: #f1f1f1; padding: 10px; border-radius: 5px;">
                    <h3>Personalized Advice:</h3>
                    {formatted_advice}
                </div>
                <p style="margin-top: 20px;">Results saved to files.</p>
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