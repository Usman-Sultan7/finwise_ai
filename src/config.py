import os
from dotenv import load_dotenv

# Load environment variables securely
load_dotenv()

# Dropdown options for Streamlit UI
GOALS = [
    "Save money", 
    "Emergency fund", 
    "Pay off debt", 
    "Vacation", 
    "Start a business", 
    "Improve budgeting"
]

CURRENCIES = ["USD ($)", "EUR (€)", "GBP (£)", "PKR (Rs)"]