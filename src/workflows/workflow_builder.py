"""Workflow builder for creating workflows programmatically"""

from typing import Dict, Any, List, Optional
from datetime import timedelta

from ..models.workflow import (
    Workflow,
    WorkflowStep,
    WorkflowTrigger,
    WorkflowStepType,
    WorkflowTriggerType,
    WorkflowStatus
)


class WorkflowBuilder:
    """Builder for creating workflows"""
    
    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description
        self.trigger: Optional[WorkflowTrigger] = None
        self.steps: List[WorkflowStep] = []
        self.previous_step: Optional[WorkflowStep] = None
    
    def add_trigger(
        self,
        trigger_type: str,
        conditions: Optional[Dict[str, Any]] = None
    ) -> "WorkflowBuilder":
        """Add a trigger to the workflow"""
        self.trigger = WorkflowTrigger(
            trigger_type=WorkflowTriggerType(trigger_type),
            conditions=conditions or {}
        )
        return self
    
    def add_email(
        self,
        template_id: str,
        name: Optional[str] = None,
        track_opens: bool = True,
        track_clicks: bool = True
    ) -> "WorkflowBuilder":
        """Add an email step"""
        step = WorkflowStep(
            step_type=WorkflowStepType.SEND_EMAIL,
            name=name or f"Send Email: {template_id}",
            template_id=template_id,
            config={
                "track_opens": track_opens,
                "track_clicks": track_clicks
            }
        )
        
        self._add_step(step)
        return self
    
    def add_delay(
        self,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        name: Optional[str] = None
    ) -> "WorkflowBuilder":
        """Add a delay step"""
        duration = timedelta(days=days, hours=hours, minutes=minutes)
        
        delay_str = []
        if days:
            delay_str.append(f"{days} day{'s' if days != 1 else ''}")
        if hours:
            delay_str.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes:
            delay_str.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        
        step = WorkflowStep(
            step_type=WorkflowStepType.DELAY,
            name=name or f"Wait {', '.join(delay_str)}",
            delay_duration=duration
        )
        
        self._add_step(step)
        return self
    
    def add_condition(
        self,
        name: str,
        condition_rules: Dict[str, Any],
        true_path: Optional[List[str]] = None,
        false_path: Optional[List[str]] = None
    ) -> "WorkflowBuilder":
        """Add a condition step"""
        step = WorkflowStep(
            step_type=WorkflowStepType.CONDITION,
            name=name,
            condition_rules=condition_rules,
            true_path=true_path,
            false_path=false_path
        )
        
        self._add_step(step)
        return self
    
    def add_tag(
        self,
        tags: List[str],
        name: Optional[str] = None
    ) -> "WorkflowBuilder":
        """Add a tag addition step"""
        step = WorkflowStep(
            step_type=WorkflowStepType.ADD_TAG,
            name=name or f"Add tags: {', '.join(tags)}",
            config={"tags": tags}
        )
        
        self._add_step(step)
        return self
    
    def remove_tag(
        self,
        tags: List[str],
        name: Optional[str] = None
    ) -> "WorkflowBuilder":
        """Add a tag removal step"""
        step = WorkflowStep(
            step_type=WorkflowStepType.REMOVE_TAG,
            name=name or f"Remove tags: {', '.join(tags)}",
            config={"tags": tags}
        )
        
        self._add_step(step)
        return self
    
    def update_field(
        self,
        updates: Dict[str, Any],
        name: Optional[str] = None
    ) -> "WorkflowBuilder":
        """Add a field update step"""
        step = WorkflowStep(
            step_type=WorkflowStepType.UPDATE_FIELD,
            name=name or "Update subscriber fields",
            config={"updates": updates}
        )
        
        self._add_step(step)
        return self
    
    def add_webhook(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None
    ) -> "WorkflowBuilder":
        """Add a webhook step"""
        step = WorkflowStep(
            step_type=WorkflowStepType.WEBHOOK,
            name=name or f"Webhook: {url}",
            config={
                "url": url,
                "data": data or {}
            }
        )
        
        self._add_step(step)
        return self
    
    def add_end(self, name: Optional[str] = None) -> "WorkflowBuilder":
        """Add an end step"""
        step = WorkflowStep(
            step_type=WorkflowStepType.END,
            name=name or "End"
        )
        
        self._add_step(step)
        return self
    
    def _add_step(self, step: WorkflowStep):
        """Add a step and link it to the previous step"""
        if self.previous_step:
            self.previous_step.next_step_id = step.id
        
        self.steps.append(step)
        self.previous_step = step
    
    def build(self) -> Workflow:
        """Build the workflow"""
        if not self.trigger:
            raise ValueError("Workflow must have a trigger")
        
        if not self.steps:
            raise ValueError("Workflow must have at least one step")
        
        workflow = Workflow(
            name=self.name,
            description=self.description,
            trigger=self.trigger,
            steps=self.steps,
            status=WorkflowStatus.DRAFT
        )
        
        return workflow


class WorkflowTemplates:
    """Pre-built workflow templates"""
    
    @staticmethod
    def welcome_series() -> WorkflowBuilder:
        """Create a welcome series workflow"""
        builder = WorkflowBuilder(
            "Welcome Series",
            "3-email welcome series for new subscribers"
        )
        
        builder.add_trigger("subscriber_joined")
        builder.add_delay(hours=1)
        builder.add_email("welcome_email", "Welcome Email")
        builder.add_delay(days=3)
        builder.add_email("getting_started", "Getting Started Guide")
        builder.add_delay(days=7)
        builder.add_email("tips_and_tricks", "Tips and Tricks")
        builder.add_tag(["welcomed"])
        
        return builder
    
    @staticmethod
    def abandoned_cart() -> WorkflowBuilder:
        """Create an abandoned cart workflow"""
        builder = WorkflowBuilder(
            "Abandoned Cart Recovery",
            "Re-engage customers who abandoned their cart"
        )
        
        builder.add_trigger("cart_abandoned")
        builder.add_delay(hours=2)
        builder.add_email("cart_reminder_1", "First Reminder")
        builder.add_delay(days=1)
        builder.add_email("cart_reminder_2", "Second Reminder with Discount")
        builder.add_delay(days=2)
        builder.add_email("cart_final_reminder", "Final Reminder")
        
        return builder
    
    @staticmethod
    def re_engagement() -> WorkflowBuilder:
        """Create a re-engagement workflow"""
        builder = WorkflowBuilder(
            "Re-engagement Campaign",
            "Win back inactive subscribers"
        )
        
        builder.add_trigger("custom_event", {"event": "inactive_subscriber"})
        builder.add_email("we_miss_you", "We Miss You")
        builder.add_delay(days=7)
        builder.add_condition(
            "Check if engaged",
            {"total_opens": 0},
            false_path=["end"],
            true_path=["special_offer"]
        )
        builder.add_email("special_offer", "Special Offer Just For You")
        builder.add_delay(days=14)
        builder.add_condition(
            "Check if still inactive",
            {"total_opens": 0},
            true_path=["unsubscribe_warning"]
        )
        builder.add_email("unsubscribe_warning", "Last Chance")
        
        return builder
    
    @staticmethod
    def birthday_campaign() -> WorkflowBuilder:
        """Create a birthday campaign workflow"""
        builder = WorkflowBuilder(
            "Birthday Campaign",
            "Send birthday wishes and special offers"
        )
        
        builder.add_trigger("date_based", {"field": "birthday"})
        builder.add_email("birthday_wishes", "Happy Birthday!")
        builder.add_tag(["birthday_2026"])
        
        return builder
