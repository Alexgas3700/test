"""
Google Sheets Client Module
Handles fetching contact data from Google Sheets
"""

import os
import logging
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleSheetsClient:
    """Client for interacting with Google Sheets API"""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    def __init__(self, credentials_path: str):
        """
        Initialize Google Sheets client
        
        Args:
            credentials_path: Path to service account credentials JSON file
        """
        self.credentials_path = credentials_path
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API using service account"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.SCOPES
            )
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Successfully authenticated with Google Sheets API")
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Sheets API: {e}")
            raise
    
    def get_contacts(
        self,
        spreadsheet_id: str,
        range_name: str = 'Sheet1!A:C'
    ) -> List[Dict[str, str]]:
        """
        Fetch contacts from Google Sheets
        
        Args:
            spreadsheet_id: The ID of the Google Spreadsheet
            range_name: The range to fetch (default: 'Sheet1!A:C')
                       Expected columns: Name, Email, Status (optional)
        
        Returns:
            List of contact dictionaries with 'name', 'email', and 'status' keys
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                logger.warning("No data found in the spreadsheet")
                return []
            
            # Parse contacts (skip header row)
            contacts = []
            headers = values[0] if values else []
            
            for row in values[1:]:
                if len(row) >= 2:  # At least name and email
                    contact = {
                        'name': row[0].strip() if row[0] else '',
                        'email': row[1].strip() if row[1] else '',
                        'status': row[2].strip() if len(row) > 2 else 'active'
                    }
                    
                    # Only include contacts with valid email and active status
                    if contact['email'] and '@' in contact['email']:
                        if contact['status'].lower() in ['active', 'subscribed', '']:
                            contacts.append(contact)
            
            logger.info(f"Successfully fetched {len(contacts)} contacts from Google Sheets")
            return contacts
            
        except HttpError as error:
            logger.error(f"An error occurred while fetching data: {error}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while fetching contacts: {e}")
            raise
    
    def validate_spreadsheet_access(self, spreadsheet_id: str) -> bool:
        """
        Validate that the spreadsheet is accessible
        
        Args:
            spreadsheet_id: The ID of the Google Spreadsheet
            
        Returns:
            True if accessible, False otherwise
        """
        try:
            self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            logger.info(f"Successfully validated access to spreadsheet {spreadsheet_id}")
            return True
        except HttpError as error:
            logger.error(f"Cannot access spreadsheet {spreadsheet_id}: {error}")
            return False
        except Exception as e:
            logger.error(f"Error validating spreadsheet access: {e}")
            return False


def main():
    """Test function for Google Sheets client"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python google_sheets_client.py <credentials_path> <spreadsheet_id>")
        sys.exit(1)
    
    credentials_path = sys.argv[1]
    spreadsheet_id = sys.argv[2]
    
    client = GoogleSheetsClient(credentials_path)
    
    if client.validate_spreadsheet_access(spreadsheet_id):
        contacts = client.get_contacts(spreadsheet_id)
        print(f"\nFetched {len(contacts)} contacts:")
        for contact in contacts[:5]:  # Show first 5
            print(f"  - {contact['name']} <{contact['email']}>")
        if len(contacts) > 5:
            print(f"  ... and {len(contacts) - 5} more")
    else:
        print("Failed to access spreadsheet")


if __name__ == '__main__':
    main()
