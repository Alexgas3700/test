"""
Workflow Example

This example demonstrates how to create and execute an automated email workflow.
"""

import asyncio
from src.models.email_template import EmailTemplate
from src.models.subscriber import Subscriber
from src.services.template_service import TemplateService
from src.services.subscriber_service import SubscriberService
from src.services.email_service import EmailService
from src.workflows.workflow_engine import WorkflowEngine
from src.workflows.workflow_builder import WorkflowBuilder, WorkflowTemplates


async def main():
    # Initialize services
    template_service = TemplateService()
    subscriber_service = SubscriberService()
    email_service = EmailService()
    workflow_engine = WorkflowEngine(
        email_service=email_service,
        template_service=template_service,
        subscriber_service=subscriber_service
    )
    
    # Step 1: Create email templates for the workflow
    print("Creating email templates...")
    
    templates = [
        EmailTemplate(
            id="welcome_email",
            name="Welcome Email",
            subject_template="Welcome to {{ company_name }}, {{ first_name }}!",
            html_content="""
            <html>
            <body>
                <h1>Welcome {{ first_name }}!</h1>
                <p>We're thrilled to have you join us.</p>
                <a href="{{ get_started_url }}">Get Started</a>
            </body>
            </html>
            """,
            required_variables=["first_name"],
            default_variables={
                "company_name": "Our Company",
                "get_started_url": "https://example.com/get-started"
            }
        ),
        EmailTemplate(
            id="getting_started",
            name="Getting Started Guide",
            subject_template="{{ first_name }}, here's how to get started",
            html_content="""
            <html>
            <body>
                <h1>Getting Started Guide</h1>
                <p>Hi {{ first_name }},</p>
                <p>Here are some tips to help you get started...</p>
            </body>
            </html>
            """,
            required_variables=["first_name"]
        ),
        EmailTemplate(
            id="tips_and_tricks",
            name="Tips and Tricks",
            subject_template="Pro tips for {{ first_name }}",
            html_content="""
            <html>
            <body>
                <h1>Tips and Tricks</h1>
                <p>Hi {{ first_name }},</p>
                <p>Here are some advanced tips to help you get the most out of our platform...</p>
            </body>
            </html>
            """,
            required_variables=["first_name"]
        )
    ]
    
    for template in templates:
        template_service.create_template(template)
        print(f"✓ Created template: {template.name}")
    
    # Step 2: Create a welcome series workflow
    print("\nCreating welcome series workflow...")
    
    builder = WorkflowBuilder("Welcome Series", "3-email welcome series for new subscribers")
    builder.add_trigger("subscriber_joined")
    builder.add_delay(hours=1)
    builder.add_email("welcome_email", "Send Welcome Email")
    builder.add_delay(days=3)
    builder.add_email("getting_started", "Send Getting Started Guide")
    builder.add_delay(days=7)
    builder.add_email("tips_and_tricks", "Send Tips and Tricks")
    builder.add_tag(["welcomed"], "Mark as welcomed")
    
    workflow = builder.build()
    workflow_engine.register_workflow(workflow)
    workflow_engine.activate_workflow(workflow.id)
    
    print(f"✓ Workflow created and activated: {workflow.id}")
    print(f"  Steps: {len(workflow.steps)}")
    
    # Step 3: Add a new subscriber
    print("\nAdding new subscriber...")
    
    subscriber = Subscriber(
        email="newuser@example.com",
        first_name="Alice",
        last_name="Johnson",
        tags=["new"]
    )
    
    subscriber_service.add_subscriber(subscriber)
    print(f"✓ Subscriber added: {subscriber.email}")
    
    # Step 4: Trigger the workflow
    print("\nTriggering workflow...")
    
    execution = await workflow_engine.trigger_workflow(
        workflow.id,
        subscriber.id,
        context={"source": "website_signup"}
    )
    
    print(f"✓ Workflow execution started: {execution.id}")
    print(f"  Status: {execution.status}")
    print(f"  Steps executed: {len(execution.step_history)}")
    
    # Step 5: Show execution history
    print("\nExecution History:")
    print(f"{'='*70}")
    for i, step in enumerate(execution.step_history, 1):
        print(f"{i}. {step['step_name']} ({step['step_type']})")
        print(f"   Status: {step['status']}")
        print(f"   Executed at: {step['executed_at']}")
        if 'error' in step:
            print(f"   Error: {step['error']}")
        print()
    
    # Step 6: Check subscriber tags
    updated_subscriber = subscriber_service.get_subscriber(subscriber.id)
    print(f"Subscriber tags after workflow: {updated_subscriber.tags}")
    
    # Example: Using pre-built workflow templates
    print("\n" + "="*70)
    print("Pre-built Workflow Templates:")
    print("="*70)
    
    # Abandoned cart workflow
    abandoned_cart = WorkflowTemplates.abandoned_cart().build()
    print(f"\n1. {abandoned_cart.name}")
    print(f"   Description: {abandoned_cart.description}")
    print(f"   Steps: {len(abandoned_cart.steps)}")
    
    # Re-engagement workflow
    re_engagement = WorkflowTemplates.re_engagement().build()
    print(f"\n2. {re_engagement.name}")
    print(f"   Description: {re_engagement.description}")
    print(f"   Steps: {len(re_engagement.steps)}")
    
    # Birthday campaign
    birthday = WorkflowTemplates.birthday_campaign().build()
    print(f"\n3. {birthday.name}")
    print(f"   Description: {birthday.description}")
    print(f"   Steps: {len(birthday.steps)}")


if __name__ == "__main__":
    asyncio.run(main())
