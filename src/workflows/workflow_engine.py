"""Workflow execution engine"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from ..models.workflow import (
    Workflow,
    WorkflowExecution,
    WorkflowStep,
    WorkflowStepType,
    WorkflowStatus,
    WorkflowTriggerType
)
from ..services.email_service import EmailService
from ..services.template_service import TemplateService
from ..services.subscriber_service import SubscriberService


class WorkflowEngine:
    """Engine for executing marketing workflows"""
    
    def __init__(
        self,
        email_service: Optional[EmailService] = None,
        template_service: Optional[TemplateService] = None,
        subscriber_service: Optional[SubscriberService] = None
    ):
        self.workflows: Dict[str, Workflow] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self.email_service = email_service or EmailService()
        self.template_service = template_service or TemplateService()
        self.subscriber_service = subscriber_service or SubscriberService()
        
        # Track subscriber workflow history
        self.subscriber_workflows: Dict[str, List[str]] = {}
    
    def register_workflow(self, workflow: Workflow) -> Workflow:
        """Register a workflow"""
        self.workflows[workflow.id] = workflow
        return workflow
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Get a workflow by ID"""
        return self.workflows.get(workflow_id)
    
    def activate_workflow(self, workflow_id: str) -> Workflow:
        """Activate a workflow"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow.status = WorkflowStatus.ACTIVE
        workflow.updated_at = datetime.utcnow()
        return workflow
    
    def pause_workflow(self, workflow_id: str) -> Workflow:
        """Pause a workflow"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow.status = WorkflowStatus.PAUSED
        workflow.updated_at = datetime.utcnow()
        return workflow
    
    async def trigger_workflow(
        self,
        workflow_id: str,
        subscriber_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowExecution:
        """Trigger a workflow for a subscriber"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        if workflow.status != WorkflowStatus.ACTIVE:
            raise ValueError(f"Workflow {workflow_id} is not active")
        
        # Check if subscriber can enter workflow
        if not self._can_enter_workflow(workflow, subscriber_id):
            raise ValueError(f"Subscriber {subscriber_id} cannot enter workflow {workflow_id}")
        
        # Create execution
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            subscriber_id=subscriber_id,
            context=context or {},
            current_step_id=workflow.steps[0].id if workflow.steps else None
        )
        
        self.executions[execution.id] = execution
        
        # Track subscriber workflow entry
        if subscriber_id not in self.subscriber_workflows:
            self.subscriber_workflows[subscriber_id] = []
        self.subscriber_workflows[subscriber_id].append(execution.id)
        
        # Update workflow stats
        workflow.total_entries += 1
        
        # Start execution
        await self._execute_workflow(execution)
        
        return execution
    
    async def _execute_workflow(self, execution: WorkflowExecution):
        """Execute a workflow"""
        workflow = self.workflows.get(execution.workflow_id)
        if not workflow:
            execution.status = "failed"
            return
        
        subscriber = self.subscriber_service.get_subscriber(execution.subscriber_id)
        if not subscriber:
            execution.status = "failed"
            return
        
        # Execute steps
        current_step_id = execution.current_step_id
        
        while current_step_id:
            step = self._get_step(workflow, current_step_id)
            if not step:
                break
            
            try:
                # Execute step
                next_step_id = await self._execute_step(
                    workflow,
                    execution,
                    step,
                    subscriber
                )
                
                # Record step in history
                execution.step_history.append({
                    "step_id": step.id,
                    "step_name": step.name,
                    "step_type": step.step_type.value,
                    "executed_at": datetime.utcnow(),
                    "status": "completed"
                })
                
                # Move to next step
                current_step_id = next_step_id
                execution.current_step_id = current_step_id
                
            except Exception as e:
                # Record error
                execution.step_history.append({
                    "step_id": step.id,
                    "step_name": step.name,
                    "step_type": step.step_type.value,
                    "executed_at": datetime.utcnow(),
                    "status": "failed",
                    "error": str(e)
                })
                execution.status = "failed"
                workflow.total_exits += 1
                return
        
        # Workflow completed
        execution.status = "completed"
        execution.completed_at = datetime.utcnow()
        workflow.total_completions += 1
    
    async def _execute_step(
        self,
        workflow: Workflow,
        execution: WorkflowExecution,
        step: WorkflowStep,
        subscriber
    ) -> Optional[str]:
        """Execute a single workflow step"""
        
        if step.step_type == WorkflowStepType.SEND_EMAIL:
            await self._execute_email_step(step, subscriber, execution)
        
        elif step.step_type == WorkflowStepType.DELAY:
            await self._execute_delay_step(step, execution)
        
        elif step.step_type == WorkflowStepType.CONDITION:
            return self._execute_condition_step(step, execution, subscriber)
        
        elif step.step_type == WorkflowStepType.ADD_TAG:
            self._execute_add_tag_step(step, subscriber)
        
        elif step.step_type == WorkflowStepType.REMOVE_TAG:
            self._execute_remove_tag_step(step, subscriber)
        
        elif step.step_type == WorkflowStepType.UPDATE_FIELD:
            self._execute_update_field_step(step, subscriber)
        
        elif step.step_type == WorkflowStepType.WEBHOOK:
            await self._execute_webhook_step(step, execution)
        
        elif step.step_type == WorkflowStepType.END:
            return None
        
        return step.next_step_id
    
    async def _execute_email_step(self, step: WorkflowStep, subscriber, execution: WorkflowExecution):
        """Execute an email step"""
        if not step.template_id:
            raise ValueError("Email step requires template_id")
        
        # Render template
        rendered = self.template_service.render_template(
            step.template_id,
            execution.context,
            subscriber_data={
                "email": subscriber.email,
                "first_name": subscriber.first_name,
                "last_name": subscriber.last_name,
                "full_name": subscriber.full_name,
                **subscriber.custom_fields
            }
        )
        
        # Send email
        await self.email_service.send_email(
            to_email=subscriber.email,
            subject=rendered["subject"],
            html_content=rendered["html"],
            text_content=rendered.get("text"),
            track_opens=step.config.get("track_opens", True),
            track_clicks=step.config.get("track_clicks", True),
            subscriber_id=subscriber.id
        )
    
    async def _execute_delay_step(self, step: WorkflowStep, execution: WorkflowExecution):
        """Execute a delay step"""
        if step.delay_duration:
            # In a real implementation, this would schedule the next step
            # For now, we'll just sleep (not recommended for production)
            execution.next_execution_at = datetime.utcnow() + step.delay_duration
            await asyncio.sleep(step.delay_duration.total_seconds())
    
    def _execute_condition_step(
        self,
        step: WorkflowStep,
        execution: WorkflowExecution,
        subscriber
    ) -> Optional[str]:
        """Execute a condition step"""
        if not step.condition_rules:
            return step.next_step_id
        
        # Evaluate condition
        condition_met = self._evaluate_condition(
            step.condition_rules,
            subscriber,
            execution.context
        )
        
        # Return appropriate path
        if condition_met and step.true_path:
            return step.true_path[0] if step.true_path else None
        elif not condition_met and step.false_path:
            return step.false_path[0] if step.false_path else None
        
        return step.next_step_id
    
    def _execute_add_tag_step(self, step: WorkflowStep, subscriber):
        """Execute an add tag step"""
        tags = step.config.get("tags", [])
        if tags:
            self.subscriber_service.add_tags(subscriber.id, tags)
    
    def _execute_remove_tag_step(self, step: WorkflowStep, subscriber):
        """Execute a remove tag step"""
        tags = step.config.get("tags", [])
        if tags:
            self.subscriber_service.remove_tags(subscriber.id, tags)
    
    def _execute_update_field_step(self, step: WorkflowStep, subscriber):
        """Execute an update field step"""
        updates = step.config.get("updates", {})
        if updates:
            self.subscriber_service.update_subscriber(subscriber.id, updates)
    
    async def _execute_webhook_step(self, step: WorkflowStep, execution: WorkflowExecution):
        """Execute a webhook step"""
        # In a real implementation, this would make an HTTP request
        # For now, we'll just log it
        webhook_url = step.config.get("url")
        webhook_data = step.config.get("data", {})
        print(f"Webhook: {webhook_url} with data: {webhook_data}")
    
    def _evaluate_condition(
        self,
        condition_rules: Dict[str, Any],
        subscriber,
        context: Dict[str, Any]
    ) -> bool:
        """Evaluate a condition"""
        # Simple condition evaluation
        # In production, you'd want a more robust rule engine
        
        for field, expected_value in condition_rules.items():
            # Check subscriber fields
            if hasattr(subscriber, field):
                actual_value = getattr(subscriber, field)
                if actual_value != expected_value:
                    return False
            
            # Check context
            elif field in context:
                if context[field] != expected_value:
                    return False
            
            else:
                return False
        
        return True
    
    def _get_step(self, workflow: Workflow, step_id: str) -> Optional[WorkflowStep]:
        """Get a step from a workflow"""
        for step in workflow.steps:
            if step.id == step_id:
                return step
        return None
    
    def _can_enter_workflow(self, workflow: Workflow, subscriber_id: str) -> bool:
        """Check if a subscriber can enter a workflow"""
        # Count how many times subscriber has entered this workflow
        subscriber_executions = self.subscriber_workflows.get(subscriber_id, [])
        workflow_entries = sum(
            1 for exec_id in subscriber_executions
            if self.executions.get(exec_id, {}).workflow_id == workflow.id
        )
        
        # Check max executions
        if workflow.max_executions_per_subscriber:
            if workflow_entries >= workflow.max_executions_per_subscriber:
                return False
        
        # Check re-entry
        if not workflow.allow_re_entry and workflow_entries > 0:
            return False
        
        return True
    
    def get_execution(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get a workflow execution"""
        return self.executions.get(execution_id)
    
    def get_subscriber_executions(self, subscriber_id: str) -> List[WorkflowExecution]:
        """Get all executions for a subscriber"""
        execution_ids = self.subscriber_workflows.get(subscriber_id, [])
        return [
            self.executions[exec_id]
            for exec_id in execution_ids
            if exec_id in self.executions
        ]
