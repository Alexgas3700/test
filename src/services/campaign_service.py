"""Campaign management service"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.campaign import Campaign, CampaignStatus
from ..models.subscriber import Subscriber
from .template_service import TemplateService
from .subscriber_service import SubscriberService
from .email_service import EmailService


class CampaignService:
    """Service for managing marketing campaigns"""
    
    def __init__(
        self,
        template_service: Optional[TemplateService] = None,
        subscriber_service: Optional[SubscriberService] = None,
        email_service: Optional[EmailService] = None
    ):
        self.campaigns: Dict[str, Campaign] = {}
        self.template_service = template_service or TemplateService()
        self.subscriber_service = subscriber_service or SubscriberService()
        self.email_service = email_service or EmailService()
    
    def create_campaign(self, campaign: Campaign) -> Campaign:
        """Create a new campaign"""
        # Validate template exists
        template = self.template_service.get_template(campaign.template_id)
        if not template:
            raise ValueError(f"Template {campaign.template_id} not found")
        
        self.campaigns[campaign.id] = campaign
        return campaign
    
    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        """Get a campaign by ID"""
        return self.campaigns.get(campaign_id)
    
    def update_campaign(self, campaign_id: str, updates: Dict[str, Any]) -> Campaign:
        """Update a campaign"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        # Don't allow updates to campaigns that are already sent
        if campaign.status == CampaignStatus.SENT:
            raise ValueError("Cannot update a campaign that has already been sent")
        
        # Update fields
        for key, value in updates.items():
            if hasattr(campaign, key):
                setattr(campaign, key, value)
        
        campaign.updated_at = datetime.utcnow()
        return campaign
    
    def delete_campaign(self, campaign_id: str) -> bool:
        """Delete a campaign"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            return False
        
        # Don't allow deletion of sent campaigns
        if campaign.status == CampaignStatus.SENT:
            raise ValueError("Cannot delete a campaign that has been sent")
        
        del self.campaigns[campaign_id]
        return True
    
    def list_campaigns(
        self,
        status: Optional[CampaignStatus] = None,
        campaign_type: Optional[str] = None
    ) -> List[Campaign]:
        """List campaigns with optional filtering"""
        campaigns = list(self.campaigns.values())
        
        if status:
            campaigns = [c for c in campaigns if c.status == status]
        
        if campaign_type:
            campaigns = [c for c in campaigns if c.campaign_type == campaign_type]
        
        return campaigns
    
    async def send_campaign(
        self,
        campaign_id: str,
        segment_filter: Optional[Dict[str, Any]] = None,
        test_mode: bool = False,
        test_emails: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send a campaign"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        # Check campaign status
        if campaign.status not in [CampaignStatus.DRAFT, CampaignStatus.SCHEDULED]:
            raise ValueError(f"Campaign cannot be sent with status: {campaign.status}")
        
        # Update status
        campaign.status = CampaignStatus.SENDING
        
        try:
            # Get recipients
            if test_mode and test_emails:
                # Test mode - send to specific emails
                recipients = []
                for email in test_emails:
                    subscriber = self.subscriber_service.get_subscriber_by_email(email)
                    if subscriber:
                        recipients.append(subscriber)
            else:
                # Get subscribers based on segment filter
                filter_criteria = segment_filter or campaign.segment_filter or {}
                recipients = self.subscriber_service.get_subscribers_by_segment(filter_criteria)
                
                # Filter by campaign type preferences
                recipients = [
                    s for s in recipients
                    if s.can_receive_campaign_type(campaign.campaign_type.value)
                ]
            
            campaign.total_recipients = len(recipients)
            
            # Prepare emails
            emails_to_send = []
            for subscriber in recipients:
                try:
                    # Render template with subscriber data
                    rendered = self.template_service.render_template(
                        campaign.template_id,
                        campaign.template_variables,
                        subscriber_data={
                            "email": subscriber.email,
                            "first_name": subscriber.first_name,
                            "last_name": subscriber.last_name,
                            "full_name": subscriber.full_name,
                            **subscriber.custom_fields
                        }
                    )
                    
                    emails_to_send.append({
                        "to_email": subscriber.email,
                        "subject": rendered["subject"],
                        "html_content": rendered["html"],
                        "text_content": rendered.get("text"),
                        "track_opens": campaign.track_opens,
                        "track_clicks": campaign.track_clicks,
                        "campaign_id": campaign.id,
                        "subscriber_id": subscriber.id
                    })
                    
                except Exception as e:
                    print(f"Error preparing email for {subscriber.email}: {str(e)}")
                    campaign.failed_count += 1
            
            # Send emails
            results = await self.email_service.send_bulk(emails_to_send)
            
            # Update campaign stats
            campaign.sent_count = results["sent"]
            campaign.failed_count += results["failed"]
            campaign.status = CampaignStatus.SENT
            campaign.updated_at = datetime.utcnow()
            
            return {
                "success": True,
                "campaign_id": campaign.id,
                "total_recipients": campaign.total_recipients,
                "sent": campaign.sent_count,
                "failed": campaign.failed_count,
                "test_mode": test_mode
            }
            
        except Exception as e:
            campaign.status = CampaignStatus.DRAFT
            raise Exception(f"Error sending campaign: {str(e)}")
    
    async def schedule_campaign(
        self,
        campaign_id: str,
        scheduled_at: datetime
    ) -> Campaign:
        """Schedule a campaign for future delivery"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        if scheduled_at <= datetime.utcnow():
            raise ValueError("Scheduled time must be in the future")
        
        campaign.scheduled_at = scheduled_at
        campaign.status = CampaignStatus.SCHEDULED
        campaign.updated_at = datetime.utcnow()
        
        return campaign
    
    def pause_campaign(self, campaign_id: str) -> Campaign:
        """Pause a campaign"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        if campaign.status != CampaignStatus.SENDING:
            raise ValueError("Can only pause campaigns that are currently sending")
        
        campaign.status = CampaignStatus.PAUSED
        campaign.updated_at = datetime.utcnow()
        
        return campaign
    
    def cancel_campaign(self, campaign_id: str) -> Campaign:
        """Cancel a campaign"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        if campaign.status == CampaignStatus.SENT:
            raise ValueError("Cannot cancel a campaign that has already been sent")
        
        campaign.status = CampaignStatus.CANCELLED
        campaign.updated_at = datetime.utcnow()
        
        return campaign
    
    def duplicate_campaign(self, campaign_id: str, new_name: str) -> Campaign:
        """Duplicate an existing campaign"""
        original = self.campaigns.get(campaign_id)
        if not original:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        # Create a copy
        duplicated_data = original.model_dump(
            exclude={
                "id", "created_at", "updated_at",
                "sent_count", "failed_count", "total_recipients"
            }
        )
        duplicated_data["name"] = new_name
        duplicated_data["status"] = CampaignStatus.DRAFT
        
        duplicated = Campaign(**duplicated_data)
        return self.create_campaign(duplicated)
