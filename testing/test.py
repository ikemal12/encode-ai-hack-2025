from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variables
API_KEY = os.getenv("API_KEY")

print(f"My API key is: {API_KEY}")  # Use the API key in your code