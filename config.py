import os
from dotenv import load_dotenv

# Load environment variables from env.txt file
load_dotenv('env.txt')

# Get the API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY or OPENAI_API_KEY == "your_api_key_here":
    print("⚠️  Warning: Please set your OpenAI API key in env.txt file")
    print("Replace 'your_api_key_here' with your actual API key")
else:
    print("✅ OpenAI API key loaded successfully") 