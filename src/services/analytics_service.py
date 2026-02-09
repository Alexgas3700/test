"""Analytics and tracking service"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

from ..models.campaign import Campaign


class CampaignStats(dict):
    """Campaign statistics"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__dict__ = self
    
    @property
    def open_rate(self) -> float:
        """Calculate open rate percentage"""
        if self.sent == 0:
            return 0.0
        return round((self.opens / self.sent) * 100, 2)
    
    @property
    def click_rate(self) -> float:
        """Calculate click rate percentage"""
        if self.sent == 0:
            return 0.0
        return round((self.clicks / self.sent) * 100, 2)
    
    @property
    def click_to_open_rate(self) -> float:
        """Calculate click-to-open rate percentage"""
        if self.unique_opens == 0:
            return 0.0
        return round((self.unique_clicks / self.unique_opens) * 100, 2)
    
    @property
    def conversion_rate(self) -> float:
        """Calculate conversion rate percentage"""
        if self.sent == 0:
            return 0.0
        return round((self.conversions / self.sent) * 100, 2)


class AnalyticsService:
    """Service for campaign analytics and tracking"""
    
    def __init__(self, email_service=None):
        self.email_service = email_service
        self.conversions: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    
    def get_campaign_stats(self, campaign_id: str) -> CampaignStats:
        """Get statistics for a campaign"""
        if not self.email_service:
            return CampaignStats(
                campaign_id=campaign_id,
                sent=0,
                opens=0,
                clicks=0,
                unique_opens=0,
                unique_clicks=0,
                conversions=0,
                bounces=0,
                complaints=0
            )
        
        # Get all emails for this campaign
        emails = self.email_service.get_sent_emails(campaign_id=campaign_id)
        
        stats = {
            "campaign_id": campaign_id,
            "sent": len(emails),
            "opens": 0,
            "clicks": 0,
            "unique_opens": 0,
            "unique_clicks": 0,
            "conversions": len(self.conversions.get(campaign_id, [])),
            "bounces": 0,
            "complaints": 0
        }
        
        opened_subscribers = set()
        clicked_subscribers = set()
        
        # Aggregate tracking data
        for email in emails:
            tracking_id = email.get("tracking_id")
            if tracking_id:
                tracking_data = self.email_service.get_tracking_data(tracking_id)
                if tracking_data:
                    if tracking_data["opened"]:
                        stats["opens"] += tracking_data["open_count"]
                        opened_subscribers.add(tracking_data["subscriber_id"])
                    
                    if tracking_data["clicked"]:
                        stats["clicks"] += tracking_data["click_count"]
                        clicked_subscribers.add(tracking_data["subscriber_id"])
        
        stats["unique_opens"] = len(opened_subscribers)
        stats["unique_clicks"] = len(clicked_subscribers)
        
        return CampaignStats(**stats)
    
    def get_campaign_timeline(
        self,
        campaign_id: str,
        interval: str = "hour"
    ) -> List[Dict[str, Any]]:
        """Get timeline of campaign events"""
        if not self.email_service:
            return []
        
        emails = self.email_service.get_sent_emails(campaign_id=campaign_id)
        
        timeline = defaultdict(lambda: {
            "timestamp": None,
            "sent": 0,
            "opens": 0,
            "clicks": 0
        })
        
        for email in emails:
            sent_at = email.get("sent_at")
            if sent_at:
                # Round to interval
                if interval == "hour":
                    bucket = sent_at.replace(minute=0, second=0, microsecond=0)
                elif interval == "day":
                    bucket = sent_at.replace(hour=0, minute=0, second=0, microsecond=0)
                else:
                    bucket = sent_at
                
                timeline[bucket]["timestamp"] = bucket
                timeline[bucket]["sent"] += 1
                
                # Add tracking data
                tracking_id = email.get("tracking_id")
                if tracking_id:
                    tracking_data = self.email_service.get_tracking_data(tracking_id)
                    if tracking_data:
                        if tracking_data["opened"]:
                            timeline[bucket]["opens"] += 1
                        if tracking_data["clicked"]:
                            timeline[bucket]["clicks"] += 1
        
        # Convert to sorted list
        return sorted(
            timeline.values(),
            key=lambda x: x["timestamp"] if x["timestamp"] else datetime.min
        )
    
    def get_link_performance(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get performance metrics for links in a campaign"""
        if not self.email_service:
            return []
        
        emails = self.email_service.get_sent_emails(campaign_id=campaign_id)
        
        link_stats = defaultdict(lambda: {
            "url": "",
            "clicks": 0,
            "unique_clicks": set()
        })
        
        for email in emails:
            tracking_id = email.get("tracking_id")
            if tracking_id:
                tracking_data = self.email_service.get_tracking_data(tracking_id)
                if tracking_data and tracking_data["clicks"]:
                    for click in tracking_data["clicks"]:
                        url = click["url"]
                        link_stats[url]["url"] = url
                        link_stats[url]["clicks"] += 1
                        link_stats[url]["unique_clicks"].add(tracking_data["subscriber_id"])
        
        # Convert to list and calculate unique clicks
        results = []
        for url, stats in link_stats.items():
            results.append({
                "url": url,
                "total_clicks": stats["clicks"],
                "unique_clicks": len(stats["unique_clicks"])
            })
        
        # Sort by total clicks
        return sorted(results, key=lambda x: x["total_clicks"], reverse=True)
    
    def track_conversion(
        self,
        campaign_id: str,
        subscriber_id: str,
        conversion_type: str,
        value: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Track a conversion event"""
        conversion = {
            "subscriber_id": subscriber_id,
            "conversion_type": conversion_type,
            "value": value,
            "metadata": metadata or {},
            "converted_at": datetime.utcnow()
        }
        
        self.conversions[campaign_id].append(conversion)
    
    def get_subscriber_engagement(
        self,
        subscriber_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get engagement metrics for a subscriber"""
        if not self.email_service:
            return {
                "subscriber_id": subscriber_id,
                "emails_received": 0,
                "emails_opened": 0,
                "emails_clicked": 0,
                "last_opened": None,
                "last_clicked": None
            }
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        emails = self.email_service.get_sent_emails(subscriber_id=subscriber_id)
        emails = [e for e in emails if e.get("sent_at", datetime.min) >= cutoff_date]
        
        engagement = {
            "subscriber_id": subscriber_id,
            "emails_received": len(emails),
            "emails_opened": 0,
            "emails_clicked": 0,
            "last_opened": None,
            "last_clicked": None
        }
        
        for email in emails:
            tracking_id = email.get("tracking_id")
            if tracking_id:
                tracking_data = self.email_service.get_tracking_data(tracking_id)
                if tracking_data:
                    if tracking_data["opened"]:
                        engagement["emails_opened"] += 1
                        if not engagement["last_opened"] or tracking_data["opened_at"] > engagement["last_opened"]:
                            engagement["last_opened"] = tracking_data["opened_at"]
                    
                    if tracking_data["clicked"]:
                        engagement["emails_clicked"] += 1
                        if not engagement["last_clicked"] or tracking_data["clicked_at"] > engagement["last_clicked"]:
                            engagement["last_clicked"] = tracking_data["clicked_at"]
        
        return engagement
    
    def compare_campaigns(
        self,
        campaign_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """Compare multiple campaigns"""
        comparison = []
        
        for campaign_id in campaign_ids:
            stats = self.get_campaign_stats(campaign_id)
            comparison.append({
                "campaign_id": campaign_id,
                "sent": stats.sent,
                "open_rate": stats.open_rate,
                "click_rate": stats.click_rate,
                "conversion_rate": stats.conversion_rate
            })
        
        return comparison
