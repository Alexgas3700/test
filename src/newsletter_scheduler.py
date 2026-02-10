"""
Newsletter Scheduler Module
Handles scheduling and execution of monthly newsletter campaigns
"""

import os
import logging
import schedule
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from google_sheets_client import GoogleSheetsClient
from email_sender import EmailSender

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/newsletter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NewsletterScheduler:
    """Scheduler for automated newsletter campaigns"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize newsletter scheduler
        
        Args:
            config_path: Path to .env configuration file (optional)
        """
        if config_path:
            load_dotenv(config_path)
        else:
            load_dotenv()
        
        # Load configuration
        self.spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')
        self.spreadsheet_range = os.getenv('GOOGLE_SPREADSHEET_RANGE', 'Sheet1!A:C')
        self.credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
        
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.sender_name = os.getenv('SENDER_NAME', 'Newsletter')
        
        self.newsletter_subject = os.getenv('NEWSLETTER_SUBJECT', 'Monthly Newsletter')
        self.newsletter_template = os.getenv('NEWSLETTER_TEMPLATE', 'newsletter.html')
        
        # Schedule configuration
        self.schedule_day = int(os.getenv('SCHEDULE_DAY_OF_MONTH', '1'))
        self.schedule_time = os.getenv('SCHEDULE_TIME', '09:00')
        
        # Validate configuration
        self._validate_config()
        
        # Initialize clients
        self.sheets_client = GoogleSheetsClient(self.credentials_path)
        self.email_sender = EmailSender(
            smtp_server=self.smtp_server,
            smtp_port=self.smtp_port,
            sender_email=self.sender_email,
            sender_password=self.sender_password,
            sender_name=self.sender_name
        )
    
    def _validate_config(self):
        """Validate required configuration"""
        required_vars = [
            'GOOGLE_SPREADSHEET_ID',
            'GOOGLE_CREDENTIALS_PATH',
            'SMTP_SERVER',
            'SENDER_EMAIL',
            'SENDER_PASSWORD'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    def send_newsletter(self):
        """Execute newsletter campaign"""
        try:
            logger.info("=" * 60)
            logger.info("Starting newsletter campaign")
            logger.info(f"Timestamp: {datetime.now().isoformat()}")
            logger.info("=" * 60)
            
            # Fetch contacts from Google Sheets
            logger.info("Fetching contacts from Google Sheets...")
            contacts = self.sheets_client.get_contacts(
                spreadsheet_id=self.spreadsheet_id,
                range_name=self.spreadsheet_range
            )
            
            if not contacts:
                logger.warning("No contacts found. Aborting newsletter campaign.")
                return
            
            logger.info(f"Found {len(contacts)} active contacts")
            
            # Send emails
            logger.info("Sending newsletter emails...")
            results = self.email_sender.send_bulk_emails(
                contacts=contacts,
                subject=self.newsletter_subject,
                template_name=self.newsletter_template,
                extra_context={
                    'month': datetime.now().strftime('%B %Y'),
                    'year': datetime.now().year
                }
            )
            
            # Log results
            logger.info("=" * 60)
            logger.info("Newsletter campaign completed")
            logger.info(f"Successfully sent: {results['sent']}")
            logger.info(f"Failed: {results['failed']}")
            logger.info(f"Total contacts: {len(contacts)}")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Error during newsletter campaign: {e}", exc_info=True)
    
    def should_run_today(self) -> bool:
        """
        Check if newsletter should run today
        
        Returns:
            True if today is the scheduled day of month
        """
        today = datetime.now().day
        return today == self.schedule_day
    
    def run_if_scheduled(self):
        """Run newsletter if today is the scheduled day"""
        if self.should_run_today():
            logger.info(f"Today is day {self.schedule_day} of the month. Running newsletter...")
            self.send_newsletter()
        else:
            logger.info(f"Today is not the scheduled day (day {self.schedule_day}). Skipping.")
    
    def start_scheduler(self):
        """Start the scheduler (runs daily and checks if it's the right day)"""
        logger.info("Starting newsletter scheduler")
        logger.info(f"Scheduled to run on day {self.schedule_day} of each month at {self.schedule_time}")
        
        # Schedule daily check
        schedule.every().day.at(self.schedule_time).do(self.run_if_scheduled)
        
        logger.info("Scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
    
    def run_now(self):
        """Run newsletter immediately (for testing)"""
        logger.info("Running newsletter immediately (manual trigger)")
        self.send_newsletter()


def main():
    """Main entry point"""
    import sys
    
    # Ensure logs directory exists
    Path('logs').mkdir(exist_ok=True)
    
    scheduler = NewsletterScheduler()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--now':
        # Run immediately for testing
        scheduler.run_now()
    elif len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Test configuration
        logger.info("Testing configuration...")
        
        # Test Google Sheets access
        if scheduler.sheets_client.validate_spreadsheet_access(scheduler.spreadsheet_id):
            logger.info("✓ Google Sheets access validated")
        else:
            logger.error("✗ Google Sheets access failed")
            sys.exit(1)
        
        # Test SMTP connection
        if scheduler.email_sender.test_connection():
            logger.info("✓ SMTP connection validated")
        else:
            logger.error("✗ SMTP connection failed")
            sys.exit(1)
        
        logger.info("✓ All tests passed")
    else:
        # Start scheduler
        scheduler.start_scheduler()


if __name__ == '__main__':
    main()
