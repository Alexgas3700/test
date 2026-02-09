"""Data models for the marketing email workflow system"""

from .campaign import Campaign, CampaignType, CampaignStatus
from .subscriber import Subscriber, SubscriberStatus
from .email_template import EmailTemplate
from .workflow import Workflow, WorkflowStep, WorkflowTrigger

__all__ = [
    "Campaign",
    "CampaignType",
    "CampaignStatus",
    "Subscriber",
    "SubscriberStatus",
    "EmailTemplate",
    "Workflow",
    "WorkflowStep",
    "WorkflowTrigger",
]
