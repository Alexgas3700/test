"""
Configuration module for newsletter system
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / 'templates'
LOGS_DIR = BASE_DIR / 'logs'
CREDENTIALS_DIR = BASE_DIR / 'credentials'

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)
CREDENTIALS_DIR.mkdir(exist_ok=True)

# Google Sheets Configuration
GOOGLE_SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID')
GOOGLE_SPREADSHEET_RANGE = os.getenv('GOOGLE_SPREADSHEET_RANGE', 'Sheet1!A:C')
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials/service-account.json')

# Email Configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
SENDER_NAME = os.getenv('SENDER_NAME', 'Newsletter')

# Newsletter Configuration
NEWSLETTER_SUBJECT = os.getenv('NEWSLETTER_SUBJECT', 'Monthly Newsletter')
NEWSLETTER_TEMPLATE = os.getenv('NEWSLETTER_TEMPLATE', 'newsletter.html')

# Schedule Configuration
SCHEDULE_DAY_OF_MONTH = int(os.getenv('SCHEDULE_DAY_OF_MONTH', '1'))
SCHEDULE_TIME = os.getenv('SCHEDULE_TIME', '09:00')


def validate_config():
    """Validate that all required configuration is present"""
    required_vars = {
        'GOOGLE_SPREADSHEET_ID': GOOGLE_SPREADSHEET_ID,
        'GOOGLE_CREDENTIALS_PATH': GOOGLE_CREDENTIALS_PATH,
        'SMTP_SERVER': SMTP_SERVER,
        'SENDER_EMAIL': SENDER_EMAIL,
        'SENDER_PASSWORD': SENDER_PASSWORD
    }
    
    missing = [key for key, value in required_vars.items() if not value]
    
    if missing:
        raise ValueError(
            f"Missing required configuration: {', '.join(missing)}\n"
            f"Please check your .env file or environment variables."
        )
    
    return True


if __name__ == '__main__':
    try:
        validate_config()
        print("✓ Configuration is valid")
        print(f"\nCurrent configuration:")
        print(f"  Spreadsheet ID: {GOOGLE_SPREADSHEET_ID}")
        print(f"  Spreadsheet Range: {GOOGLE_SPREADSHEET_RANGE}")
        print(f"  SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")
        print(f"  Sender Email: {SENDER_EMAIL}")
        print(f"  Schedule: Day {SCHEDULE_DAY_OF_MONTH} at {SCHEDULE_TIME}")
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
