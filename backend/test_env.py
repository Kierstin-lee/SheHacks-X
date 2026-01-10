from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")

# Test output
if api_key:
    print("OPENAI_API_KEY loaded successfully!")
else:
    print("OPENAI_API_KEY NOT found. Check your .env file location and format.")
