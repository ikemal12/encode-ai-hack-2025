import os
from dotenv import load_dotenv
from portia import (
    Config,
    LLMModel,
    LLMProvider,
    Portia,
    example_tool_registry,
)

# Load your environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Set up Portia config with Gemini 2.0 Flash
google_config = Config.from_default(
    llm_provider=LLMProvider.GOOGLE_GENERATIVE_AI,
    llm_model_name=LLMModel.GEMINI_2_0_FLASH,
    google_api_key=GOOGLE_API_KEY
)

# Initialize Portia with example tools
portia = Portia(config=google_config, tools=example_tool_registry)

# Query to run
query = "add 1 + 2"
plan_run = portia.run(query)

# Try to extract the result (adjust this key if needed)
try:
    # Commonly used field name
    result = plan_run.final_output
except AttributeError:
    try:
        result = plan_run.output
    except AttributeError:
        # As a last resort, print full structure to investigate
        print("Could not find result in 'final_output' or 'output'. Dumping full structure:")
        print(plan_run.model_dump_json(indent=2))
        result = "?"

# Format the math expression
expression = query.replace("add ", "")
print(f"{expression} = {result}")