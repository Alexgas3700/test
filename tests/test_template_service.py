"""Tests for template service"""

import pytest
from src.models.email_template import EmailTemplate
from src.services.template_service import TemplateService


def test_create_template():
    """Test creating a template"""
    service = TemplateService()
    
    template = EmailTemplate(
        name="Test Template",
        subject_template="Hello {{ name }}",
        html_content="<p>Hello {{ name }}</p>",
        required_variables=["name"]
    )
    
    result = service.create_template(template)
    assert result.id == template.id
    assert result.name == "Test Template"


def test_render_template():
    """Test rendering a template"""
    service = TemplateService()
    
    template = EmailTemplate(
        name="Test Template",
        subject_template="Hello {{ name }}",
        html_content="<p>Hello {{ name }}</p>",
        required_variables=["name"]
    )
    
    service.create_template(template)
    
    rendered = service.render_template(
        template.id,
        {"name": "John"}
    )
    
    assert rendered["subject"] == "Hello John"
    assert rendered["html"] == "<p>Hello John</p>"


def test_missing_required_variables():
    """Test that missing required variables raise an error"""
    service = TemplateService()
    
    template = EmailTemplate(
        name="Test Template",
        subject_template="Hello {{ name }}",
        html_content="<p>Hello {{ name }}</p>",
        required_variables=["name"]
    )
    
    service.create_template(template)
    
    with pytest.raises(ValueError):
        service.render_template(template.id, {})


def test_default_variables():
    """Test that default variables are used"""
    service = TemplateService()
    
    template = EmailTemplate(
        name="Test Template",
        subject_template="Hello {{ name }}",
        html_content="<p>Hello {{ name }}</p>",
        default_variables={"name": "Guest"}
    )
    
    service.create_template(template)
    
    rendered = service.render_template(template.id, {})
    assert rendered["subject"] == "Hello Guest"


def test_validate_template():
    """Test template validation"""
    service = TemplateService()
    
    # Valid template
    valid_template = EmailTemplate(
        name="Valid",
        subject_template="Hello",
        html_content="<p>Hello</p>"
    )
    
    result = service.validate_template(valid_template)
    assert result["valid"] is True
    
    # Invalid template (bad Jinja syntax)
    invalid_template = EmailTemplate(
        name="Invalid",
        subject_template="Hello {{ name",
        html_content="<p>Hello</p>"
    )
    
    result = service.validate_template(invalid_template)
    assert result["valid"] is False
    assert len(result["errors"]) > 0
