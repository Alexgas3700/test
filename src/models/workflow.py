"""Workflow data model"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field
import uuid


class WorkflowTriggerType(str, Enum):
    """Types of workflow triggers"""
    SUBSCRIBER_JOINED = "subscriber_joined"
    TAG_ADDED = "tag_added"
    TAG_REMOVED = "tag_removed"
    EMAIL_OPENED = "email_opened"
    EMAIL_CLICKED = "email_clicked"
    PURCHASE_MADE = "purchase_made"
    CART_ABANDONED = "cart_abandoned"
    DATE_BASED = "date_based"
    CUSTOM_EVENT = "custom_event"


class WorkflowStepType(str, Enum):
    """Types of workflow steps"""
    SEND_EMAIL = "send_email"
    DELAY = "delay"
    CONDITION = "condition"
    ADD_TAG = "add_tag"
    REMOVE_TAG = "remove_tag"
    UPDATE_FIELD = "update_field"
    WEBHOOK = "webhook"
    END = "end"


class WorkflowStatus(str, Enum):
    """Workflow status"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class WorkflowTrigger(BaseModel):
    """Workflow trigger configuration"""
    
    trigger_type: WorkflowTriggerType
    conditions: Dict[str, Any] = Field(
        default_factory=dict,
        description="Conditions that must be met for trigger to fire"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "trigger_type": "subscriber_joined",
                "conditions": {
                    "tags": ["new_customer"],
                    "source": "website"
                }
            }
        }


class WorkflowStep(BaseModel):
    """Individual step in a workflow"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    step_type: WorkflowStepType
    name: str = Field(..., description="Step name")
    
    # Step configuration
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Step-specific configuration"
    )
    
    # For delay steps
    delay_duration: Optional[timedelta] = None
    
    # For email steps
    template_id: Optional[str] = None
    
    # For condition steps
    condition_rules: Optional[Dict[str, Any]] = None
    true_path: Optional[List[str]] = Field(
        default=None,
        description="Step IDs to execute if condition is true"
    )
    false_path: Optional[List[str]] = Field(
        default=None,
        description="Step IDs to execute if condition is false"
    )
    
    # Next step
    next_step_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "step_type": "send_email",
                "name": "Send Welcome Email",
                "template_id": "welcome_email_001",
                "config": {
                    "track_opens": True,
                    "track_clicks": True
                }
            }
        }


class Workflow(BaseModel):
    """Marketing workflow model"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="Workflow name")
    description: Optional[str] = None
    
    # Workflow configuration
    trigger: WorkflowTrigger
    steps: List[WorkflowStep] = Field(default_factory=list)
    
    # Status
    status: WorkflowStatus = Field(default=WorkflowStatus.DRAFT)
    
    # Execution settings
    max_executions_per_subscriber: Optional[int] = Field(
        default=1,
        description="How many times a subscriber can enter this workflow"
    )
    allow_re_entry: bool = Field(
        default=False,
        description="Can subscribers re-enter after completion"
    )
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    
    # Analytics
    total_entries: int = Field(default=0)
    total_completions: int = Field(default=0)
    total_exits: int = Field(default=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Welcome Series",
                "description": "3-email welcome series for new subscribers",
                "trigger": {
                    "trigger_type": "subscriber_joined",
                    "conditions": {}
                },
                "status": "active",
                "allow_re_entry": False
            }
        }


class WorkflowExecution(BaseModel):
    """Track individual workflow executions"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: str
    subscriber_id: str
    
    # Execution state
    current_step_id: Optional[str] = None
    status: str = Field(default="running")  # running, completed, failed, cancelled
    
    # Timing
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    next_execution_at: Optional[datetime] = None
    
    # Context data
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Data passed between workflow steps"
    )
    
    # History
    step_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of executed steps"
    )
