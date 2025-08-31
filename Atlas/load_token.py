from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the token from the environment
REMOVED = os.getenv("REMOVED")

# Just to check it worked (optional)
print("Your token is:", REMOVED)
