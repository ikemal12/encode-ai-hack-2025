from flask import Flask, request, render_template, send_from_directory
import os
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    salary = request.form['salary']
    debt = request.form['debt']
    savings = request.form['savings']
    
    # Store in variables
    financial_data = {
        'salary': salary,
        'debt': debt,
        'savings': savings
    }
    
    # Write to file
    with open("financial_data.txt", "w") as f:
        for key, value in financial_data.items():
            f.write(f"{key}: {value}\n")
    
    # Initialize Portia
    google_config = Config.from_default(
        llm_provider=LLMProvider.GOOGLE_GENERATIVE_AI,
        llm_model_name=LLMModel.GEMINI_2_0_FLASH,
        google_api_key=GOOGLE_API_KEY
    )
    portia = Portia(config=google_config, tools=example_tool_registry)
    
    # Use the financial data in your Portia query
    plan_run = portia.run(f'Analyze financial data: Salary {salary}, Debt {debt}, Savings {savings}')
    final_output_value = plan_run.outputs.final_output.value
    
    with open("output.txt", "w") as f:
        f.write(f"{final_output_value}\n")
    
    return f"""
        Data received and processed!<br>
        Salary: £{salary}<br>
        Debt: £{debt}<br>
        Savings: £{savings}<br>
        Results written to files.
    """

# Route to serve static files from frontend folder
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)