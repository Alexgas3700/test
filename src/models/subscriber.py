"""Subscriber data model"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, EmailStr
import uuid


class SubscriberStatus(str, Enum):
    """Subscriber status"""
    ACTIVE = "active"
    UNSUBSCRIBED = "unsubscribed"
    BOUNCED = "bounced"
    COMPLAINED = "complained"
    PENDING = "pending"


class Subscriber(BaseModel):
    """Subscriber model"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr = Field(..., description="Subscriber email address")
    
    # Personal information
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    
    # Status and preferences
    status: SubscriberStatus = Field(default=SubscriberStatus.ACTIVE)
    tags: List[str] = Field(default_factory=list)
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    
    # Segmentation
    segments: List[str] = Field(default_factory=list)
    
    # Preferences
    email_preferences: Dict[str, bool] = Field(
        default_factory=lambda: {
            "promotional": True,
            "newsletter": True,
            "transactional": True
        }
    )
    
    # Engagement metrics
    total_opens: int = Field(default=0)
    total_clicks: int = Field(default=0)
    last_opened_at: Optional[datetime] = None
    last_clicked_at: Optional[datetime] = None
    
    # Metadata
    subscribed_at: datetime = Field(default_factory=datetime.utcnow)
    unsubscribed_at: Optional[datetime] = None
    source: Optional[str] = Field(
        default=None,
        description="How the subscriber was acquired"
    )
    
    # GDPR and compliance
    consent_given: bool = Field(default=True)
    consent_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    ip_address: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "customer@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "tags": ["premium", "active"],
                "custom_fields": {
                    "company": "Acme Corp",
                    "industry": "Technology"
                },
                "segments": ["high_value", "engaged"],
                "source": "website_signup"
            }
        }
    
    @property
    def full_name(self) -> str:
        """Get full name"""
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return " ".join(parts) if parts else self.email
    
    def is_active(self) -> bool:
        """Check if subscriber is active"""
        return self.status == SubscriberStatus.ACTIVE
    
    def can_receive_campaign_type(self, campaign_type: str) -> bool:
        """Check if subscriber can receive a specific campaign type"""
        if not self.is_active():
            return False
        
        # Transactional emails can always be sent
        if campaign_type == "transactional":
            return True
        
        # Check preferences for other types
        return self.email_preferences.get(campaign_type, False)
