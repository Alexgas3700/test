"""Tests for workflow builder"""

import pytest
from datetime import timedelta
from src.workflows.workflow_builder import WorkflowBuilder, WorkflowTemplates
from src.models.workflow import WorkflowStepType


def test_build_simple_workflow():
    """Test building a simple workflow"""
    builder = WorkflowBuilder("Test Workflow")
    builder.add_trigger("subscriber_joined")
    builder.add_email("welcome_email")
    
    workflow = builder.build()
    
    assert workflow.name == "Test Workflow"
    assert len(workflow.steps) == 1
    assert workflow.steps[0].step_type == WorkflowStepType.SEND_EMAIL


def test_workflow_with_delay():
    """Test workflow with delay steps"""
    builder = WorkflowBuilder("Test Workflow")
    builder.add_trigger("subscriber_joined")
    builder.add_delay(days=1)
    builder.add_email("email1")
    builder.add_delay(hours=2)
    builder.add_email("email2")
    
    workflow = builder.build()
    
    assert len(workflow.steps) == 4
    assert workflow.steps[0].step_type == WorkflowStepType.DELAY
    assert workflow.steps[0].delay_duration == timedelta(days=1)
    assert workflow.steps[2].delay_duration == timedelta(hours=2)


def test_workflow_with_tags():
    """Test workflow with tag operations"""
    builder = WorkflowBuilder("Test Workflow")
    builder.add_trigger("subscriber_joined")
    builder.add_tag(["new_customer"])
    builder.add_email("welcome")
    builder.remove_tag(["prospect"])
    
    workflow = builder.build()
    
    assert len(workflow.steps) == 3
    assert workflow.steps[0].step_type == WorkflowStepType.ADD_TAG
    assert workflow.steps[2].step_type == WorkflowStepType.REMOVE_TAG


def test_workflow_linking():
    """Test that steps are properly linked"""
    builder = WorkflowBuilder("Test Workflow")
    builder.add_trigger("subscriber_joined")
    builder.add_email("email1")
    builder.add_delay(days=1)
    builder.add_email("email2")
    
    workflow = builder.build()
    
    # First step should link to second
    assert workflow.steps[0].next_step_id == workflow.steps[1].id
    # Second step should link to third
    assert workflow.steps[1].next_step_id == workflow.steps[2].id


def test_welcome_series_template():
    """Test welcome series template"""
    builder = WorkflowTemplates.welcome_series()
    workflow = builder.build()
    
    assert workflow.name == "Welcome Series"
    assert len(workflow.steps) > 0


def test_abandoned_cart_template():
    """Test abandoned cart template"""
    builder = WorkflowTemplates.abandoned_cart()
    workflow = builder.build()
    
    assert workflow.name == "Abandoned Cart Recovery"
    assert len(workflow.steps) > 0


def test_workflow_without_trigger():
    """Test that workflow without trigger raises error"""
    builder = WorkflowBuilder("Test Workflow")
    builder.add_email("email1")
    
    with pytest.raises(ValueError):
        builder.build()


def test_workflow_without_steps():
    """Test that workflow without steps raises error"""
    builder = WorkflowBuilder("Test Workflow")
    builder.add_trigger("subscriber_joined")
    
    with pytest.raises(ValueError):
        builder.build()
