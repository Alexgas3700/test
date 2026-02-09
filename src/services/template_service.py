"""Email template service"""

from typing import Dict, Any, List, Optional
from jinja2 import Environment, Template, TemplateError
from datetime import datetime

from ..models.email_template import EmailTemplate


class TemplateService:
    """Service for managing and rendering email templates"""
    
    def __init__(self):
        self.templates: Dict[str, EmailTemplate] = {}
        self.jinja_env = Environment(autoescape=True)
    
    def create_template(self, template: EmailTemplate) -> EmailTemplate:
        """Create a new email template"""
        # Validate template syntax
        try:
            Template(template.html_content)
            Template(template.subject_template)
            if template.text_content:
                Template(template.text_content)
        except TemplateError as e:
            raise ValueError(f"Invalid template syntax: {str(e)}")
        
        self.templates[template.id] = template
        return template
    
    def get_template(self, template_id: str) -> Optional[EmailTemplate]:
        """Get a template by ID"""
        return self.templates.get(template_id)
    
    def update_template(self, template_id: str, updates: Dict[str, Any]) -> EmailTemplate:
        """Update an existing template"""
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Update fields
        for key, value in updates.items():
            if hasattr(template, key):
                setattr(template, key, value)
        
        template.updated_at = datetime.utcnow()
        return template
    
    def delete_template(self, template_id: str) -> bool:
        """Delete a template"""
        if template_id in self.templates:
            del self.templates[template_id]
            return True
        return False
    
    def list_templates(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        active_only: bool = True
    ) -> List[EmailTemplate]:
        """List templates with optional filtering"""
        templates = list(self.templates.values())
        
        if active_only:
            templates = [t for t in templates if t.is_active]
        
        if category:
            templates = [t for t in templates if t.category == category]
        
        if tags:
            templates = [
                t for t in templates
                if any(tag in t.tags for tag in tags)
            ]
        
        return templates
    
    def render_template(
        self,
        template_id: str,
        variables: Dict[str, Any],
        subscriber_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """Render a template with variables"""
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Merge variables with defaults and subscriber data
        render_vars = {**template.default_variables}
        if subscriber_data:
            render_vars.update(subscriber_data)
        render_vars.update(variables)
        
        # Check for required variables
        missing_vars = [
            var for var in template.required_variables
            if var not in render_vars
        ]
        if missing_vars:
            raise ValueError(f"Missing required variables: {', '.join(missing_vars)}")
        
        # Render templates
        try:
            subject_tmpl = self.jinja_env.from_string(template.subject_template)
            html_tmpl = self.jinja_env.from_string(template.html_content)
            
            rendered = {
                "subject": subject_tmpl.render(**render_vars),
                "html": html_tmpl.render(**render_vars),
            }
            
            if template.text_content:
                text_tmpl = self.jinja_env.from_string(template.text_content)
                rendered["text"] = text_tmpl.render(**render_vars)
            
            if template.preheader:
                preheader_tmpl = self.jinja_env.from_string(template.preheader)
                rendered["preheader"] = preheader_tmpl.render(**render_vars)
            
            # Increment usage counter
            template.times_used += 1
            
            return rendered
            
        except TemplateError as e:
            raise ValueError(f"Error rendering template: {str(e)}")
    
    def validate_template(self, template: EmailTemplate) -> Dict[str, Any]:
        """Validate a template and return validation results"""
        results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check template syntax
        try:
            Template(template.html_content)
        except TemplateError as e:
            results["valid"] = False
            results["errors"].append(f"HTML content error: {str(e)}")
        
        try:
            Template(template.subject_template)
        except TemplateError as e:
            results["valid"] = False
            results["errors"].append(f"Subject template error: {str(e)}")
        
        if template.text_content:
            try:
                Template(template.text_content)
            except TemplateError as e:
                results["valid"] = False
                results["errors"].append(f"Text content error: {str(e)}")
        
        # Check for best practices
        if len(template.subject_template) > 60:
            results["warnings"].append("Subject line is longer than 60 characters")
        
        if not template.text_content:
            results["warnings"].append("No plain text version provided")
        
        if "unsubscribe" not in template.html_content.lower():
            results["warnings"].append("No unsubscribe link found in template")
        
        return results
    
    def clone_template(self, template_id: str, new_name: str) -> EmailTemplate:
        """Clone an existing template"""
        original = self.get_template(template_id)
        if not original:
            raise ValueError(f"Template {template_id} not found")
        
        # Create a copy
        cloned_data = original.model_dump(exclude={"id", "created_at", "updated_at", "times_used"})
        cloned_data["name"] = new_name
        
        cloned = EmailTemplate(**cloned_data)
        return self.create_template(cloned)
