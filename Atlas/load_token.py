from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the token from the environment
HF_TOKEN = os.getenv("HF_TOKEN")

# Just to check it worked (optional)
print("Your token is:", HF_TOKEN)
