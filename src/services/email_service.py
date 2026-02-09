"""Email sending service"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib
import base64

from ..models.subscriber import Subscriber
from ..models.campaign import Campaign


class EmailService:
    """Service for sending emails"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.sent_emails: List[Dict[str, Any]] = []
        self.tracking_data: Dict[str, Dict[str, Any]] = {}
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
        track_opens: bool = True,
        track_clicks: bool = True,
        campaign_id: Optional[str] = None,
        subscriber_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send an email"""
        
        # Generate tracking ID
        tracking_id = self._generate_tracking_id(to_email, campaign_id)
        
        # Add tracking pixels and links if enabled
        if track_opens:
            html_content = self._add_open_tracking(html_content, tracking_id)
        
        if track_clicks:
            html_content = self._add_click_tracking(html_content, tracking_id)
        
        # Prepare email data
        email_data = {
            "to": to_email,
            "from": from_email or self.config.get("default_from_email", "noreply@example.com"),
            "from_name": from_name or self.config.get("default_from_name", "Marketing Team"),
            "subject": subject,
            "html": html_content,
            "text": text_content,
            "tracking_id": tracking_id,
            "campaign_id": campaign_id,
            "subscriber_id": subscriber_id,
            "sent_at": datetime.utcnow(),
            "status": "sent"
        }
        
        # In a real implementation, this would use SMTP or an email service API
        # For now, we'll just store the email data
        self.sent_emails.append(email_data)
        
        # Initialize tracking data
        self.tracking_data[tracking_id] = {
            "email": to_email,
            "campaign_id": campaign_id,
            "subscriber_id": subscriber_id,
            "sent_at": email_data["sent_at"],
            "opened": False,
            "opened_at": None,
            "open_count": 0,
            "clicked": False,
            "clicked_at": None,
            "click_count": 0,
            "clicks": []
        }
        
        return {
            "success": True,
            "tracking_id": tracking_id,
            "message_id": tracking_id
        }
    
    async def send_bulk(
        self,
        emails: List[Dict[str, Any]],
        rate_limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Send bulk emails with optional rate limiting"""
        
        results = {
            "total": len(emails),
            "sent": 0,
            "failed": 0,
            "errors": []
        }
        
        # Apply rate limiting if specified
        delay = 1.0 / rate_limit if rate_limit else 0
        
        for email_data in emails:
            try:
                await self.send_email(**email_data)
                results["sent"] += 1
                
                if delay > 0:
                    await asyncio.sleep(delay)
                    
            except Exception as e:
                results["failed"] += 1
                results["errors"].append({
                    "email": email_data.get("to_email"),
                    "error": str(e)
                })
        
        return results
    
    def track_open(self, tracking_id: str) -> bool:
        """Track email open"""
        if tracking_id in self.tracking_data:
            data = self.tracking_data[tracking_id]
            if not data["opened"]:
                data["opened"] = True
                data["opened_at"] = datetime.utcnow()
            data["open_count"] += 1
            return True
        return False
    
    def track_click(self, tracking_id: str, url: str) -> bool:
        """Track email click"""
        if tracking_id in self.tracking_data:
            data = self.tracking_data[tracking_id]
            if not data["clicked"]:
                data["clicked"] = True
                data["clicked_at"] = datetime.utcnow()
            data["click_count"] += 1
            data["clicks"].append({
                "url": url,
                "clicked_at": datetime.utcnow()
            })
            return True
        return False
    
    def get_tracking_data(self, tracking_id: str) -> Optional[Dict[str, Any]]:
        """Get tracking data for an email"""
        return self.tracking_data.get(tracking_id)
    
    def _generate_tracking_id(self, email: str, campaign_id: Optional[str]) -> str:
        """Generate a unique tracking ID"""
        data = f"{email}:{campaign_id}:{datetime.utcnow().isoformat()}"
        hash_obj = hashlib.sha256(data.encode())
        return base64.urlsafe_b64encode(hash_obj.digest()).decode()[:16]
    
    def _add_open_tracking(self, html_content: str, tracking_id: str) -> str:
        """Add open tracking pixel to HTML content"""
        tracking_pixel = f'<img src="https://track.example.com/open/{tracking_id}" width="1" height="1" alt="" />'
        
        # Try to add before closing body tag
        if "</body>" in html_content:
            html_content = html_content.replace("</body>", f"{tracking_pixel}</body>")
        else:
            html_content += tracking_pixel
        
        return html_content
    
    def _add_click_tracking(self, html_content: str, tracking_id: str) -> str:
        """Add click tracking to links in HTML content"""
        # This is a simplified implementation
        # In production, you'd use a proper HTML parser
        
        import re
        
        def replace_link(match):
            original_url = match.group(1)
            tracked_url = f"https://track.example.com/click/{tracking_id}?url={original_url}"
            return f'href="{tracked_url}"'
        
        # Replace href attributes
        html_content = re.sub(
            r'href="([^"]+)"',
            replace_link,
            html_content
        )
        
        return html_content
    
    def get_sent_emails(
        self,
        campaign_id: Optional[str] = None,
        subscriber_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get sent emails with optional filtering"""
        emails = self.sent_emails
        
        if campaign_id:
            emails = [e for e in emails if e.get("campaign_id") == campaign_id]
        
        if subscriber_id:
            emails = [e for e in emails if e.get("subscriber_id") == subscriber_id]
        
        return emails
