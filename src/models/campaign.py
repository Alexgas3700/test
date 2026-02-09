"""Campaign data model"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
import uuid


class CampaignType(str, Enum):
    """Types of marketing campaigns"""
    PROMOTIONAL = "promotional"
    NEWSLETTER = "newsletter"
    TRANSACTIONAL = "transactional"
    WELCOME_SERIES = "welcome_series"
    ABANDONED_CART = "abandoned_cart"
    RE_ENGAGEMENT = "re_engagement"
    ANNOUNCEMENT = "announcement"


class CampaignStatus(str, Enum):
    """Campaign status"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class Campaign(BaseModel):
    """Marketing campaign model"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="Campaign name")
    subject: str = Field(..., description="Email subject line")
    campaign_type: CampaignType = Field(..., description="Type of campaign")
    status: CampaignStatus = Field(default=CampaignStatus.DRAFT)
    
    # Template and content
    template_id: str = Field(..., description="Email template ID")
    template_variables: Dict[str, Any] = Field(default_factory=dict)
    
    # Targeting
    segment_filter: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Filter criteria for targeting subscribers"
    )
    tags: List[str] = Field(default_factory=list)
    
    # Scheduling
    scheduled_at: Optional[datetime] = Field(
        default=None,
        description="When to send the campaign"
    )
    send_immediately: bool = Field(default=False)
    
    # Tracking
    track_opens: bool = Field(default=True)
    track_clicks: bool = Field(default=True)
    
    # A/B Testing
    ab_test_enabled: bool = Field(default=False)
    ab_test_variants: Optional[List[Dict[str, Any]]] = Field(default=None)
    ab_test_percentage: Optional[int] = Field(
        default=None,
        ge=1,
        le=100,
        description="Percentage of audience for A/B test"
    )
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    
    # Analytics (populated after sending)
    total_recipients: int = Field(default=0)
    sent_count: int = Field(default=0)
    failed_count: int = Field(default=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Summer Sale 2026",
                "subject": "Get 50% Off This Summer!",
                "campaign_type": "promotional",
                "template_id": "summer_sale",
                "template_variables": {
                    "discount_code": "SUMMER50",
                    "expiry_date": "2026-08-31"
                },
                "tags": ["sale", "summer"],
                "send_immediately": False,
                "scheduled_at": "2026-06-01T10:00:00Z"
            }
        }
