"""
Segmentation Example

This example demonstrates how to segment subscribers and send targeted campaigns.
"""

import asyncio
from src.models.subscriber import Subscriber
from src.models.campaign import Campaign, CampaignType
from src.models.email_template import EmailTemplate
from src.services.subscriber_service import SubscriberService
from src.services.template_service import TemplateService
from src.services.campaign_service import CampaignService
from src.services.email_service import EmailService


async def main():
    # Initialize services
    subscriber_service = SubscriberService()
    template_service = TemplateService()
    email_service = EmailService()
    campaign_service = CampaignService(
        template_service=template_service,
        subscriber_service=subscriber_service,
        email_service=email_service
    )
    
    # Step 1: Add subscribers with different attributes
    print("Adding subscribers with different segments...")
    
    subscribers = [
        # Premium customers
        Subscriber(
            email="premium1@example.com",
            first_name="Alice",
            tags=["premium", "active"],
            segments=["high_value"],
            custom_fields={"lifetime_value": 5000, "industry": "Technology"}
        ),
        Subscriber(
            email="premium2@example.com",
            first_name="Bob",
            tags=["premium", "active"],
            segments=["high_value"],
            custom_fields={"lifetime_value": 7500, "industry": "Finance"}
        ),
        
        # Regular customers
        Subscriber(
            email="regular1@example.com",
            first_name="Charlie",
            tags=["active"],
            segments=["engaged"],
            custom_fields={"lifetime_value": 500, "industry": "Retail"}
        ),
        Subscriber(
            email="regular2@example.com",
            first_name="Diana",
            tags=["active"],
            segments=["engaged"],
            custom_fields={"lifetime_value": 750, "industry": "Healthcare"}
        ),
        
        # Inactive customers
        Subscriber(
            email="inactive1@example.com",
            first_name="Eve",
            tags=["inactive"],
            segments=["needs_engagement"],
            custom_fields={"lifetime_value": 100, "industry": "Education"}
        )
    ]
    
    for subscriber in subscribers:
        subscriber_service.add_subscriber(subscriber)
        print(f"✓ Added: {subscriber.email} - Tags: {subscriber.tags}")
    
    # Step 2: Create targeted templates
    print("\nCreating targeted templates...")
    
    templates = {
        "premium_offer": EmailTemplate(
            name="Premium Exclusive Offer",
            subject_template="{{ first_name }}, exclusive VIP offer inside!",
            html_content="""
            <html>
            <body>
                <h1>VIP Exclusive Offer</h1>
                <p>Hi {{ first_name }},</p>
                <p>As a valued premium member, we're offering you an exclusive 30% discount!</p>
                <p>Your lifetime value: ${{ lifetime_value }}</p>
            </body>
            </html>
            """,
            required_variables=["first_name"],
            category="promotional"
        ),
        "regular_offer": EmailTemplate(
            name="Regular Customer Offer",
            subject_template="{{ first_name }}, special offer for you!",
            html_content="""
            <html>
            <body>
                <h1>Special Offer</h1>
                <p>Hi {{ first_name }},</p>
                <p>Get 15% off your next purchase!</p>
            </body>
            </html>
            """,
            required_variables=["first_name"],
            category="promotional"
        ),
        "winback": EmailTemplate(
            name="Win-back Campaign",
            subject_template="We miss you, {{ first_name }}!",
            html_content="""
            <html>
            <body>
                <h1>We Miss You!</h1>
                <p>Hi {{ first_name }},</p>
                <p>It's been a while! Come back and get 20% off to welcome you back.</p>
            </body>
            </html>
            """,
            required_variables=["first_name"],
            category="re_engagement"
        )
    }
    
    for key, template in templates.items():
        template_service.create_template(template)
        print(f"✓ Created template: {template.name}")
    
    # Step 3: Create and send targeted campaigns
    print("\n" + "="*70)
    print("Sending Targeted Campaigns")
    print("="*70)
    
    # Campaign 1: Premium customers only
    print("\n1. Campaign for Premium Customers:")
    premium_campaign = Campaign(
        name="VIP Exclusive Offer",
        subject="Exclusive VIP Offer",
        campaign_type=CampaignType.PROMOTIONAL,
        template_id=templates["premium_offer"].id,
        segment_filter={
            "tags": ["premium"],
            "status": "active"
        }
    )
    
    campaign_service.create_campaign(premium_campaign)
    result = await campaign_service.send_campaign(premium_campaign.id)
    print(f"   Recipients: {result['total_recipients']}")
    print(f"   Sent: {result['sent']}")
    
    # Campaign 2: Regular active customers
    print("\n2. Campaign for Regular Customers:")
    regular_campaign = Campaign(
        name="Regular Customer Offer",
        subject="Special Offer",
        campaign_type=CampaignType.PROMOTIONAL,
        template_id=templates["regular_offer"].id,
        segment_filter={
            "tags": ["active"],
            "tags_all": []  # Active but not premium
        }
    )
    
    campaign_service.create_campaign(regular_campaign)
    result = await campaign_service.send_campaign(regular_campaign.id)
    print(f"   Recipients: {result['total_recipients']}")
    print(f"   Sent: {result['sent']}")
    
    # Campaign 3: Inactive customers (win-back)
    print("\n3. Win-back Campaign for Inactive Customers:")
    winback_campaign = Campaign(
        name="Win-back Campaign",
        subject="We Miss You!",
        campaign_type=CampaignType.RE_ENGAGEMENT,
        template_id=templates["winback"].id,
        segment_filter={
            "tags": ["inactive"]
        }
    )
    
    campaign_service.create_campaign(winback_campaign)
    result = await campaign_service.send_campaign(winback_campaign.id)
    print(f"   Recipients: {result['total_recipients']}")
    print(f"   Sent: {result['sent']}")
    
    # Step 4: Advanced segmentation examples
    print("\n" + "="*70)
    print("Advanced Segmentation Examples")
    print("="*70)
    
    # High-value customers in Technology industry
    print("\n1. High-value Technology customers:")
    tech_high_value = subscriber_service.get_subscribers_by_segment({
        "segments": ["high_value"],
        "custom_fields": {"industry": "Technology"}
    })
    print(f"   Found: {len(tech_high_value)} subscribers")
    for sub in tech_high_value:
        print(f"   - {sub.email} (LTV: ${sub.custom_fields.get('lifetime_value')})")
    
    # Engaged customers with minimum lifetime value
    print("\n2. Engaged customers with LTV > $500:")
    engaged_valuable = subscriber_service.get_subscribers_by_segment({
        "segments": ["engaged"]
    })
    engaged_valuable = [
        s for s in engaged_valuable
        if s.custom_fields.get("lifetime_value", 0) > 500
    ]
    print(f"   Found: {len(engaged_valuable)} subscribers")
    for sub in engaged_valuable:
        print(f"   - {sub.email} (LTV: ${sub.custom_fields.get('lifetime_value')})")
    
    # Step 5: Dynamic segmentation
    print("\n" + "="*70)
    print("Dynamic Segmentation Based on Engagement")
    print("="*70)
    
    # Simulate some engagement
    print("\nSimulating engagement...")
    subscriber_service.update_engagement("premium1@example.com", opened=True, clicked=True)
    subscriber_service.update_engagement("regular1@example.com", opened=True)
    
    # Find highly engaged subscribers
    print("\nHighly engaged subscribers (opened AND clicked):")
    all_subscribers = subscriber_service.list_subscribers()
    highly_engaged = [
        s for s in all_subscribers
        if s.total_opens > 0 and s.total_clicks > 0
    ]
    print(f"   Found: {len(highly_engaged)} subscribers")
    for sub in highly_engaged:
        print(f"   - {sub.email} (Opens: {sub.total_opens}, Clicks: {sub.total_clicks})")


if __name__ == "__main__":
    asyncio.run(main())
