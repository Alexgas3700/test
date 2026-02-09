# Quick Start Guide

This guide will help you get started with the Marketing Email Workflow System in just a few minutes.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Basic Usage

### 1. Run Your First Campaign

```bash
python examples/basic_campaign.py
```

This example demonstrates:
- Creating an email template
- Adding subscribers
- Creating a campaign
- Sending emails to a segment
- Viewing campaign statistics

### 2. Try Automated Workflows

```bash
python examples/workflow_example.py
```

This example shows:
- Building a welcome series workflow
- Triggering workflows automatically
- Using pre-built workflow templates

### 3. Explore Segmentation

```bash
python examples/segmentation_example.py
```

Learn how to:
- Segment subscribers by tags and attributes
- Send targeted campaigns
- Use custom fields for advanced segmentation

### 4. Analyze Campaign Performance

```bash
python examples/analytics_example.py
```

Discover how to:
- Track opens and clicks
- Measure campaign performance
- Compare multiple campaigns
- Identify segments for follow-up

## Key Features

### Campaign Management

Create and send marketing campaigns:

```python
from src.models.campaign import Campaign, CampaignType
from src.services.campaign_service import CampaignService

campaign = Campaign(
    name="Summer Sale",
    subject="Get 50% Off!",
    campaign_type=CampaignType.PROMOTIONAL,
    template_id="summer_sale_template",
    segment_filter={"tags": ["active"]}
)

campaign_service = CampaignService()
campaign_service.create_campaign(campaign)
await campaign_service.send_campaign(campaign.id)
```

### Workflow Automation

Build automated email sequences:

```python
from src.workflows.workflow_builder import WorkflowBuilder

builder = WorkflowBuilder("Welcome Series")
builder.add_trigger("subscriber_joined")
builder.add_delay(hours=1)
builder.add_email("welcome_email")
builder.add_delay(days=3)
builder.add_email("getting_started")

workflow = builder.build()
```

### Subscriber Management

Manage your subscriber list:

```python
from src.models.subscriber import Subscriber
from src.services.subscriber_service import SubscriberService

subscriber = Subscriber(
    email="customer@example.com",
    first_name="John",
    tags=["premium", "active"]
)

subscriber_service = SubscriberService()
subscriber_service.add_subscriber(subscriber)
```

### Analytics & Tracking

Track campaign performance:

```python
from src.services.analytics_service import AnalyticsService

analytics = AnalyticsService()
stats = analytics.get_campaign_stats(campaign_id)

print(f"Open Rate: {stats.open_rate}%")
print(f"Click Rate: {stats.click_rate}%")
```

## Pre-built Workflow Templates

Use ready-made workflow templates:

```python
from src.workflows.workflow_builder import WorkflowTemplates

# Welcome series
welcome = WorkflowTemplates.welcome_series().build()

# Abandoned cart recovery
cart = WorkflowTemplates.abandoned_cart().build()

# Re-engagement campaign
reengagement = WorkflowTemplates.re_engagement().build()

# Birthday campaign
birthday = WorkflowTemplates.birthday_campaign().build()
```

## Email Templates

The system includes beautiful, responsive email templates:

- `welcome.html` - Welcome new subscribers
- `promotional.html` - Promotional offers and sales
- `newsletter.html` - Regular content updates
- `base.html` - Base template for customization

All templates support variable substitution using Jinja2 syntax.

## Configuration

Create a `config.json` file in `src/config/`:

```json
{
  "smtp": {
    "host": "smtp.example.com",
    "port": 587,
    "username": "your_username",
    "password": "your_password",
    "use_tls": true
  },
  "tracking": {
    "enabled": true,
    "track_opens": true,
    "track_clicks": true
  }
}
```

Or use environment variables:

```bash
export SMTP_HOST=smtp.example.com
export SMTP_PORT=587
export SMTP_USERNAME=your_username
export SMTP_PASSWORD=your_password
```

## Running Tests

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=src --cov-report=html
```

## Next Steps

1. **Customize Templates**: Edit the HTML templates in `src/templates/` to match your brand
2. **Create Workflows**: Build custom workflows for your specific use cases
3. **Integrate**: Connect the system to your database and email service provider
4. **Scale**: Implement background job processing for large campaigns

## Common Use Cases

### Welcome New Subscribers

```python
# Automatically send welcome emails when someone subscribes
workflow = WorkflowTemplates.welcome_series().build()
engine.register_workflow(workflow)
engine.activate_workflow(workflow.id)
```

### Recover Abandoned Carts

```python
# Send reminders to customers who abandoned their cart
workflow = WorkflowTemplates.abandoned_cart().build()
engine.register_workflow(workflow)
```

### Re-engage Inactive Users

```python
# Win back subscribers who haven't engaged recently
workflow = WorkflowTemplates.re_engagement().build()
engine.register_workflow(workflow)
```

### Send Promotional Campaigns

```python
# Target specific segments with promotional offers
campaign = Campaign(
    name="Flash Sale",
    campaign_type=CampaignType.PROMOTIONAL,
    segment_filter={"tags": ["premium"], "min_opens": 5}
)
```

## Support

For more information, see the full documentation in `README.md`.

## Best Practices

1. **Always include unsubscribe links** in your templates
2. **Test campaigns** before sending to your full list
3. **Segment your audience** for better engagement
4. **Track performance** and optimize based on data
5. **Respect rate limits** to maintain deliverability
6. **Follow email regulations** (GDPR, CAN-SPAM, etc.)

Happy emailing! 📧
