"""
Basic Campaign Example

This example demonstrates how to create and send a simple marketing campaign.
"""

import asyncio
from datetime import datetime
from src.models.campaign import Campaign, CampaignType
from src.models.email_template import EmailTemplate
from src.models.subscriber import Subscriber
from src.services.template_service import TemplateService
from src.services.subscriber_service import SubscriberService
from src.services.campaign_service import CampaignService
from src.services.email_service import EmailService


async def main():
    # Initialize services
    template_service = TemplateService()
    subscriber_service = SubscriberService()
    email_service = EmailService()
    campaign_service = CampaignService(
        template_service=template_service,
        subscriber_service=subscriber_service,
        email_service=email_service
    )
    
    # Step 1: Create an email template
    print("Creating email template...")
    template = EmailTemplate(
        name="Summer Sale",
        description="Summer sale promotional email",
        subject_template="🌞 {{ first_name }}, Get {{ discount }}% Off This Summer!",
        html_content="""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h1>Summer Sale!</h1>
            <p>Hi {{ first_name }},</p>
            <p>We're excited to offer you <strong>{{ discount }}% off</strong> on all products!</p>
            <p>Use code: <strong>{{ promo_code }}</strong></p>
            <a href="{{ shop_url }}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Shop Now
            </a>
            <p>Offer valid until {{ expiry_date }}</p>
            <p><a href="{{ unsubscribe_url }}">Unsubscribe</a></p>
        </body>
        </html>
        """,
        required_variables=["first_name", "discount", "promo_code", "shop_url", "expiry_date"],
        default_variables={
            "shop_url": "https://example.com/shop",
            "unsubscribe_url": "https://example.com/unsubscribe"
        },
        category="promotional"
    )
    
    template_service.create_template(template)
    print(f"✓ Template created: {template.id}")
    
    # Step 2: Add subscribers
    print("\nAdding subscribers...")
    subscribers = [
        Subscriber(
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            tags=["premium", "active"]
        ),
        Subscriber(
            email="jane.smith@example.com",
            first_name="Jane",
            last_name="Smith",
            tags=["active"]
        ),
        Subscriber(
            email="bob.wilson@example.com",
            first_name="Bob",
            last_name="Wilson",
            tags=["premium"]
        )
    ]
    
    for subscriber in subscribers:
        subscriber_service.add_subscriber(subscriber)
        print(f"✓ Added subscriber: {subscriber.email}")
    
    # Step 3: Create a campaign
    print("\nCreating campaign...")
    campaign = Campaign(
        name="Summer Sale 2026",
        subject="Get 50% Off This Summer!",
        campaign_type=CampaignType.PROMOTIONAL,
        template_id=template.id,
        template_variables={
            "discount": "50",
            "promo_code": "SUMMER50",
            "expiry_date": "August 31, 2026"
        },
        segment_filter={
            "status": "active",
            "tags": ["active"]
        },
        track_opens=True,
        track_clicks=True
    )
    
    campaign_service.create_campaign(campaign)
    print(f"✓ Campaign created: {campaign.id}")
    
    # Step 4: Send the campaign
    print("\nSending campaign...")
    result = await campaign_service.send_campaign(campaign.id)
    
    print(f"\n{'='*50}")
    print("Campaign Results:")
    print(f"{'='*50}")
    print(f"Total Recipients: {result['total_recipients']}")
    print(f"Sent: {result['sent']}")
    print(f"Failed: {result['failed']}")
    print(f"{'='*50}")
    
    # Step 5: Check campaign stats
    from src.services.analytics_service import AnalyticsService
    analytics = AnalyticsService(email_service=email_service)
    
    print("\nCampaign Statistics:")
    stats = analytics.get_campaign_stats(campaign.id)
    print(f"Sent: {stats.sent}")
    print(f"Opens: {stats.opens} (Unique: {stats.unique_opens})")
    print(f"Clicks: {stats.clicks} (Unique: {stats.unique_clicks})")
    print(f"Open Rate: {stats.open_rate}%")
    print(f"Click Rate: {stats.click_rate}%")


if __name__ == "__main__":
    asyncio.run(main())
