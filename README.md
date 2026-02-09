# Marketing Email Workflow System

A comprehensive marketing email workflow system for managing campaigns, subscribers, and automated email sequences.

## Features

- **Campaign Management**: Create and manage marketing email campaigns
- **Subscriber Management**: Handle subscriber lists, segments, and preferences
- **Email Templates**: Customizable HTML email templates with variable substitution
- **Workflow Automation**: Define automated email sequences and triggers
- **Analytics & Tracking**: Track opens, clicks, and conversions
- **Unsubscribe Management**: Handle opt-outs and preferences
- **Scheduling**: Schedule campaigns for future delivery

## Project Structure

```
.
├── src/
│   ├── config/           # Configuration files
│   ├── models/           # Data models
│   ├── services/         # Business logic
│   ├── templates/        # Email templates
│   ├── workflows/        # Workflow definitions
│   └── utils/            # Utility functions
├── examples/             # Usage examples
├── tests/                # Test files
└── README.md
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Create a Campaign

```python
from src.services.campaign_service import CampaignService
from src.models.campaign import Campaign, CampaignType

campaign_service = CampaignService()

campaign = Campaign(
    name="Summer Sale 2026",
    subject="Get 50% Off This Summer!",
    campaign_type=CampaignType.PROMOTIONAL,
    template_id="summer_sale"
)

campaign_service.create_campaign(campaign)
```

### 2. Add Subscribers

```python
from src.services.subscriber_service import SubscriberService
from src.models.subscriber import Subscriber

subscriber_service = SubscriberService()

subscriber = Subscriber(
    email="customer@example.com",
    first_name="John",
    last_name="Doe",
    tags=["premium", "active"]
)

subscriber_service.add_subscriber(subscriber)
```

### 3. Create a Workflow

```python
from src.workflows.workflow_engine import WorkflowEngine
from src.workflows.workflow_builder import WorkflowBuilder

builder = WorkflowBuilder("Welcome Series")
builder.add_trigger("subscriber_joined")
builder.add_delay(hours=1)
builder.add_email("welcome_email")
builder.add_delay(days=3)
builder.add_email("getting_started")
builder.add_delay(days=7)
builder.add_email("tips_and_tricks")

workflow = builder.build()
engine = WorkflowEngine()
engine.register_workflow(workflow)
```

### 4. Send a Campaign

```python
from src.services.campaign_service import CampaignService

campaign_service = CampaignService()
campaign_service.send_campaign(
    campaign_id="campaign_123",
    segment_filter={"tags": ["premium"]}
)
```

## Configuration

Create a `config.json` file in the `src/config/` directory:

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
  },
  "rate_limiting": {
    "max_emails_per_hour": 1000,
    "max_emails_per_day": 10000
  }
}
```

## Email Templates

Templates support Jinja2 syntax for variable substitution:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ subject }}</title>
</head>
<body>
    <h1>Hello {{ first_name }}!</h1>
    <p>{{ message }}</p>
    <a href="{{ cta_link }}">{{ cta_text }}</a>
</body>
</html>
```

## Workflow Types

### Welcome Series
Automatically send a series of emails to new subscribers.

### Abandoned Cart
Re-engage customers who left items in their cart.

### Re-engagement
Win back inactive subscribers.

### Promotional
Send time-sensitive offers and promotions.

### Newsletter
Regular content updates to your subscriber base.

## Analytics

Track campaign performance:

```python
from src.services.analytics_service import AnalyticsService

analytics = AnalyticsService()
stats = analytics.get_campaign_stats("campaign_123")

print(f"Sent: {stats.sent}")
print(f"Opens: {stats.opens} ({stats.open_rate}%)")
print(f"Clicks: {stats.clicks} ({stats.click_rate}%)")
print(f"Conversions: {stats.conversions}")
```

## Best Practices

1. **Segment Your Audience**: Target specific groups for better engagement
2. **A/B Testing**: Test subject lines and content
3. **Personalization**: Use subscriber data to personalize emails
4. **Mobile Optimization**: Ensure templates are mobile-responsive
5. **Compliance**: Follow GDPR, CAN-SPAM, and other regulations
6. **Unsubscribe Links**: Always include an easy way to opt-out
7. **Rate Limiting**: Respect sending limits to maintain deliverability

## API Reference

See the full API documentation in the `docs/` directory.

## License

MIT License
