import os
from dotenv import load_dotenv
from portia import (
    Config,
    LLMModel,
    LLMProvider,
    Portia,
    example_tool_registry,
)

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Create a default Portia config with LLM provider set to Google GenAI and model set to Gemini 2.0 Flash
google_config = Config.from_default(
    llm_provider=LLMProvider.GOOGLE_GENERATIVE_AI,
    llm_model_name=LLMModel.GEMINI_2_0_FLASH,
    google_api_key=GOOGLE_API_KEY
)
# Instantiate a Portia instance. Load it with the config and with the example tools.
portia = Portia(config=google_config, tools=example_tool_registry)
plan_run = portia.run('add 1 + 2')
final_output_value = plan_run.outputs.final_output.value

with open("output.txt", "w") as f:
    f.write(f"{final_output_value}\n")

print("Output written to output.txt")