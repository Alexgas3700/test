"""
Analytics Example

This example demonstrates how to track and analyze campaign performance.
"""

import asyncio
from datetime import datetime, timedelta
from src.models.subscriber import Subscriber
from src.models.campaign import Campaign, CampaignType
from src.models.email_template import EmailTemplate
from src.services.subscriber_service import SubscriberService
from src.services.template_service import TemplateService
from src.services.campaign_service import CampaignService
from src.services.email_service import EmailService
from src.services.analytics_service import AnalyticsService


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
    analytics_service = AnalyticsService(email_service=email_service)
    
    # Step 1: Setup
    print("Setting up campaign and subscribers...")
    
    # Create template
    template = EmailTemplate(
        name="Product Launch",
        subject_template="🚀 {{ first_name }}, check out our new product!",
        html_content="""
        <html>
        <body>
            <h1>New Product Launch!</h1>
            <p>Hi {{ first_name }},</p>
            <p>We're excited to announce our new product!</p>
            <a href="https://example.com/product">Learn More</a>
            <a href="https://example.com/buy">Buy Now</a>
        </body>
        </html>
        """,
        required_variables=["first_name"]
    )
    template_service.create_template(template)
    
    # Add subscribers
    subscribers = []
    for i in range(10):
        subscriber = Subscriber(
            email=f"user{i}@example.com",
            first_name=f"User{i}",
            tags=["active"]
        )
        subscriber_service.add_subscriber(subscriber)
        subscribers.append(subscriber)
    
    # Create and send campaign
    campaign = Campaign(
        name="Product Launch Campaign",
        subject="New Product Launch",
        campaign_type=CampaignType.ANNOUNCEMENT,
        template_id=template.id,
        template_variables={},
        segment_filter={"tags": ["active"]}
    )
    campaign_service.create_campaign(campaign)
    await campaign_service.send_campaign(campaign.id)
    
    print(f"✓ Campaign sent to {len(subscribers)} subscribers")
    
    # Step 2: Simulate engagement
    print("\nSimulating user engagement...")
    
    sent_emails = email_service.get_sent_emails(campaign_id=campaign.id)
    
    # Simulate opens (70% open rate)
    for i, email in enumerate(sent_emails[:7]):
        tracking_id = email["tracking_id"]
        email_service.track_open(tracking_id)
        if i < 3:  # Some users open multiple times
            email_service.track_open(tracking_id)
        print(f"✓ Tracked open: {email['to']}")
    
    # Simulate clicks (30% click rate)
    for i, email in enumerate(sent_emails[:3]):
        tracking_id = email["tracking_id"]
        email_service.track_click(tracking_id, "https://example.com/product")
        print(f"✓ Tracked click: {email['to']}")
    
    # Simulate conversions
    for i, email in enumerate(sent_emails[:2]):
        subscriber_id = email["subscriber_id"]
        analytics_service.track_conversion(
            campaign.id,
            subscriber_id,
            "purchase",
            value=99.99
        )
        print(f"✓ Tracked conversion: {email['to']}")
    
    # Step 3: Analyze campaign performance
    print("\n" + "="*70)
    print("Campaign Performance Analysis")
    print("="*70)
    
    stats = analytics_service.get_campaign_stats(campaign.id)
    
    print(f"\nOverall Statistics:")
    print(f"  Total Sent: {stats.sent}")
    print(f"  Total Opens: {stats.opens}")
    print(f"  Unique Opens: {stats.unique_opens}")
    print(f"  Total Clicks: {stats.clicks}")
    print(f"  Unique Clicks: {stats.unique_clicks}")
    print(f"  Conversions: {stats.conversions}")
    print(f"\nPerformance Metrics:")
    print(f"  Open Rate: {stats.open_rate}%")
    print(f"  Click Rate: {stats.click_rate}%")
    print(f"  Click-to-Open Rate: {stats.click_to_open_rate}%")
    print(f"  Conversion Rate: {stats.conversion_rate}%")
    
    # Step 4: Link performance
    print("\n" + "="*70)
    print("Link Performance")
    print("="*70)
    
    link_performance = analytics_service.get_link_performance(campaign.id)
    for i, link in enumerate(link_performance, 1):
        print(f"\n{i}. {link['url']}")
        print(f"   Total Clicks: {link['total_clicks']}")
        print(f"   Unique Clicks: {link['unique_clicks']}")
    
    # Step 5: Subscriber engagement analysis
    print("\n" + "="*70)
    print("Top Engaged Subscribers")
    print("="*70)
    
    # Update subscriber engagement metrics
    for email in sent_emails:
        tracking_data = email_service.get_tracking_data(email["tracking_id"])
        if tracking_data:
            subscriber_service.update_engagement(
                email["subscriber_id"],
                opened=tracking_data["opened"],
                clicked=tracking_data["clicked"]
            )
    
    # Get engagement for each subscriber
    print("\nSubscriber Engagement (Last 30 days):")
    for subscriber in subscribers[:5]:  # Show top 5
        engagement = analytics_service.get_subscriber_engagement(subscriber.id, days=30)
        print(f"\n{subscriber.email}:")
        print(f"  Emails Received: {engagement['emails_received']}")
        print(f"  Emails Opened: {engagement['emails_opened']}")
        print(f"  Emails Clicked: {engagement['emails_clicked']}")
        if engagement['last_opened']:
            print(f"  Last Opened: {engagement['last_opened']}")
    
    # Step 6: Compare multiple campaigns
    print("\n" + "="*70)
    print("Campaign Comparison")
    print("="*70)
    
    # Create another campaign for comparison
    campaign2 = Campaign(
        name="Follow-up Campaign",
        subject="Follow-up",
        campaign_type=CampaignType.PROMOTIONAL,
        template_id=template.id,
        template_variables={},
        segment_filter={"tags": ["active"]}
    )
    campaign_service.create_campaign(campaign2)
    await campaign_service.send_campaign(campaign2.id)
    
    # Simulate different engagement for campaign 2
    sent_emails2 = email_service.get_sent_emails(campaign_id=campaign2.id)
    for email in sent_emails2[:5]:
        email_service.track_open(email["tracking_id"])
    for email in sent_emails2[:2]:
        email_service.track_click(email["tracking_id"], "https://example.com/product")
    
    # Compare campaigns
    comparison = analytics_service.compare_campaigns([campaign.id, campaign2.id])
    
    print(f"\n{'Campaign':<30} {'Sent':<10} {'Open Rate':<12} {'Click Rate':<12} {'Conv Rate':<12}")
    print("-" * 76)
    for comp in comparison:
        print(f"{comp['campaign_id'][:28]:<30} {comp['sent']:<10} {comp['open_rate']:<11.2f}% {comp['click_rate']:<11.2f}% {comp['conversion_rate']:<11.2f}%")
    
    # Step 7: Identify segments for follow-up
    print("\n" + "="*70)
    print("Segmentation for Follow-up Campaigns")
    print("="*70)
    
    all_subscribers = subscriber_service.list_subscribers()
    
    # Opened but didn't click
    opened_no_click = [
        s for s in all_subscribers
        if s.total_opens > 0 and s.total_clicks == 0
    ]
    print(f"\nOpened but didn't click: {len(opened_no_click)} subscribers")
    print("  → Send: More information about the product")
    
    # Clicked but didn't convert
    clicked_no_conversion = [
        s for s in all_subscribers
        if s.total_clicks > 0
    ]
    # Filter out those who converted
    conversions = analytics_service.conversions.get(campaign.id, [])
    converted_ids = {c["subscriber_id"] for c in conversions}
    clicked_no_conversion = [
        s for s in clicked_no_conversion
        if s.id not in converted_ids
    ]
    print(f"\nClicked but didn't convert: {len(clicked_no_conversion)} subscribers")
    print("  → Send: Special discount offer")
    
    # Didn't open
    didnt_open = [
        s for s in all_subscribers
        if s.total_opens == 0
    ]
    print(f"\nDidn't open: {len(didnt_open)} subscribers")
    print("  → Send: Different subject line or time")


if __name__ == "__main__":
    asyncio.run(main())
