"""Email template data model"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
import uuid


class EmailTemplate(BaseModel):
    """Email template model"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="Template name")
    description: Optional[str] = None
    
    # Template content
    subject_template: str = Field(..., description="Subject line template")
    html_content: str = Field(..., description="HTML email content")
    text_content: Optional[str] = Field(
        default=None,
        description="Plain text version"
    )
    
    # Template variables
    required_variables: List[str] = Field(
        default_factory=list,
        description="List of required template variables"
    )
    default_variables: Dict[str, Any] = Field(
        default_factory=dict,
        description="Default values for variables"
    )
    
    # Styling
    preheader: Optional[str] = Field(
        default=None,
        description="Email preheader text"
    )
    
    # Categorization
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    is_active: bool = Field(default=True)
    
    # Usage tracking
    times_used: int = Field(default=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Welcome Email",
                "description": "Welcome new subscribers",
                "subject_template": "Welcome to {{ company_name }}, {{ first_name }}!",
                "html_content": "<html><body><h1>Welcome {{ first_name }}!</h1></body></html>",
                "required_variables": ["first_name", "company_name"],
                "default_variables": {
                    "company_name": "Our Company"
                },
                "category": "onboarding",
                "tags": ["welcome", "onboarding"]
            }
        }
