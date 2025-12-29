import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Retrieve the GRID API key
grid_api_key = os.getenv("GRID_API_KEY")

if grid_api_key:
    print(f"Successfully loaded GRID API key: {grid_api_key[:4]}...")
else:
    print("Failed to load GRID_API_KEY. Make sure it is set in the .env file.")
