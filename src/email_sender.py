"""
Email Sender Module
Handles sending emails with template support
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSender:
    """Email sender with template support"""
    
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        sender_email: str,
        sender_password: str,
        sender_name: Optional[str] = None,
        use_tls: bool = True
    ):
        """
        Initialize email sender
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP server port
            sender_email: Sender email address
            sender_password: Sender email password or app password
            sender_name: Sender display name (optional)
            use_tls: Whether to use TLS (default: True)
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sender_name = sender_name or sender_email
        self.use_tls = use_tls
        
        # Setup Jinja2 template environment
        template_dir = Path(__file__).parent.parent / 'templates'
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
    
    def render_template(
        self,
        template_name: str,
        context: Dict[str, any]
    ) -> str:
        """
        Render email template with context
        
        Args:
            template_name: Name of the template file
            context: Dictionary with template variables
            
        Returns:
            Rendered HTML content
        """
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            logger.error(f"Error rendering template {template_name}: {e}")
            raise
    
    def send_email(
        self,
        recipient_email: str,
        recipient_name: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Send email to a single recipient
        
        Args:
            recipient_email: Recipient email address
            recipient_name: Recipient name
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text email content (optional)
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = f"{self.sender_name} <{self.sender_email}>"
            message['To'] = f"{recipient_name} <{recipient_email}>"
            
            # Add plain text version if provided
            if text_content:
                part1 = MIMEText(text_content, 'plain')
                message.attach(part1)
            
            # Add HTML version
            part2 = MIMEText(html_content, 'html')
            message.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            logger.info(f"Successfully sent email to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {e}")
            return False
    
    def send_bulk_emails(
        self,
        contacts: List[Dict[str, str]],
        subject: str,
        template_name: str,
        extra_context: Optional[Dict[str, any]] = None
    ) -> Dict[str, int]:
        """
        Send emails to multiple recipients using a template
        
        Args:
            contacts: List of contact dictionaries with 'name' and 'email' keys
            subject: Email subject
            template_name: Name of the template file to use
            extra_context: Additional context variables for template (optional)
            
        Returns:
            Dictionary with 'sent' and 'failed' counts
        """
        results = {'sent': 0, 'failed': 0}
        
        for contact in contacts:
            try:
                # Prepare context for this recipient
                context = {
                    'recipient_name': contact.get('name', 'Subscriber'),
                    'recipient_email': contact.get('email'),
                    **(extra_context or {})
                }
                
                # Render template
                html_content = self.render_template(template_name, context)
                
                # Send email
                success = self.send_email(
                    recipient_email=contact['email'],
                    recipient_name=contact.get('name', 'Subscriber'),
                    subject=subject,
                    html_content=html_content
                )
                
                if success:
                    results['sent'] += 1
                else:
                    results['failed'] += 1
                    
            except Exception as e:
                logger.error(f"Error processing contact {contact.get('email')}: {e}")
                results['failed'] += 1
        
        logger.info(f"Bulk email completed: {results['sent']} sent, {results['failed']} failed")
        return results
    
    def test_connection(self) -> bool:
        """
        Test SMTP connection
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.sender_email, self.sender_password)
            logger.info("SMTP connection test successful")
            return True
        except Exception as e:
            logger.error(f"SMTP connection test failed: {e}")
            return False


def main():
    """Test function for email sender"""
    import sys
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Test SMTP connection
    sender = EmailSender(
        smtp_server=os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        smtp_port=int(os.getenv('SMTP_PORT', '587')),
        sender_email=os.getenv('SENDER_EMAIL'),
        sender_password=os.getenv('SENDER_PASSWORD'),
        sender_name=os.getenv('SENDER_NAME', 'Newsletter')
    )
    
    if sender.test_connection():
        print("✓ SMTP connection successful")
    else:
        print("✗ SMTP connection failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
