"""Subscriber management service"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.subscriber import Subscriber, SubscriberStatus


class SubscriberService:
    """Service for managing subscribers"""
    
    def __init__(self):
        self.subscribers: Dict[str, Subscriber] = {}
        self.email_index: Dict[str, str] = {}  # email -> subscriber_id
    
    def add_subscriber(self, subscriber: Subscriber) -> Subscriber:
        """Add a new subscriber"""
        # Check if email already exists
        if subscriber.email in self.email_index:
            existing_id = self.email_index[subscriber.email]
            raise ValueError(f"Subscriber with email {subscriber.email} already exists (ID: {existing_id})")
        
        self.subscribers[subscriber.id] = subscriber
        self.email_index[subscriber.email] = subscriber.id
        return subscriber
    
    def get_subscriber(self, subscriber_id: str) -> Optional[Subscriber]:
        """Get a subscriber by ID"""
        return self.subscribers.get(subscriber_id)
    
    def get_subscriber_by_email(self, email: str) -> Optional[Subscriber]:
        """Get a subscriber by email"""
        subscriber_id = self.email_index.get(email)
        if subscriber_id:
            return self.subscribers.get(subscriber_id)
        return None
    
    def update_subscriber(self, subscriber_id: str, updates: Dict[str, Any]) -> Subscriber:
        """Update subscriber information"""
        subscriber = self.subscribers.get(subscriber_id)
        if not subscriber:
            raise ValueError(f"Subscriber {subscriber_id} not found")
        
        # Don't allow email updates through this method
        if "email" in updates:
            raise ValueError("Email cannot be updated directly")
        
        # Update fields
        for key, value in updates.items():
            if hasattr(subscriber, key):
                setattr(subscriber, key, value)
        
        return subscriber
    
    def unsubscribe(self, subscriber_id: str, reason: Optional[str] = None) -> Subscriber:
        """Unsubscribe a subscriber"""
        subscriber = self.subscribers.get(subscriber_id)
        if not subscriber:
            raise ValueError(f"Subscriber {subscriber_id} not found")
        
        subscriber.status = SubscriberStatus.UNSUBSCRIBED
        subscriber.unsubscribed_at = datetime.utcnow()
        
        if reason:
            subscriber.custom_fields["unsubscribe_reason"] = reason
        
        return subscriber
    
    def resubscribe(self, subscriber_id: str) -> Subscriber:
        """Resubscribe a subscriber"""
        subscriber = self.subscribers.get(subscriber_id)
        if not subscriber:
            raise ValueError(f"Subscriber {subscriber_id} not found")
        
        subscriber.status = SubscriberStatus.ACTIVE
        subscriber.unsubscribed_at = None
        subscriber.subscribed_at = datetime.utcnow()
        
        return subscriber
    
    def add_tags(self, subscriber_id: str, tags: List[str]) -> Subscriber:
        """Add tags to a subscriber"""
        subscriber = self.subscribers.get(subscriber_id)
        if not subscriber:
            raise ValueError(f"Subscriber {subscriber_id} not found")
        
        for tag in tags:
            if tag not in subscriber.tags:
                subscriber.tags.append(tag)
        
        return subscriber
    
    def remove_tags(self, subscriber_id: str, tags: List[str]) -> Subscriber:
        """Remove tags from a subscriber"""
        subscriber = self.subscribers.get(subscriber_id)
        if not subscriber:
            raise ValueError(f"Subscriber {subscriber_id} not found")
        
        subscriber.tags = [t for t in subscriber.tags if t not in tags]
        return subscriber
    
    def update_engagement(
        self,
        subscriber_id: str,
        opened: bool = False,
        clicked: bool = False
    ) -> Subscriber:
        """Update subscriber engagement metrics"""
        subscriber = self.subscribers.get(subscriber_id)
        if not subscriber:
            raise ValueError(f"Subscriber {subscriber_id} not found")
        
        if opened:
            subscriber.total_opens += 1
            subscriber.last_opened_at = datetime.utcnow()
        
        if clicked:
            subscriber.total_clicks += 1
            subscriber.last_clicked_at = datetime.utcnow()
        
        return subscriber
    
    def get_subscribers_by_segment(
        self,
        segment_filter: Dict[str, Any]
    ) -> List[Subscriber]:
        """Get subscribers matching segment criteria"""
        subscribers = list(self.subscribers.values())
        
        # Filter by status
        if "status" in segment_filter:
            status = segment_filter["status"]
            subscribers = [s for s in subscribers if s.status == status]
        
        # Filter by tags (any match)
        if "tags" in segment_filter:
            required_tags = segment_filter["tags"]
            subscribers = [
                s for s in subscribers
                if any(tag in s.tags for tag in required_tags)
            ]
        
        # Filter by tags (all match)
        if "tags_all" in segment_filter:
            required_tags = segment_filter["tags_all"]
            subscribers = [
                s for s in subscribers
                if all(tag in s.tags for tag in required_tags)
            ]
        
        # Filter by segments
        if "segments" in segment_filter:
            required_segments = segment_filter["segments"]
            subscribers = [
                s for s in subscribers
                if any(seg in s.segments for seg in required_segments)
            ]
        
        # Filter by custom fields
        if "custom_fields" in segment_filter:
            for field, value in segment_filter["custom_fields"].items():
                subscribers = [
                    s for s in subscribers
                    if s.custom_fields.get(field) == value
                ]
        
        # Filter by engagement
        if "min_opens" in segment_filter:
            min_opens = segment_filter["min_opens"]
            subscribers = [s for s in subscribers if s.total_opens >= min_opens]
        
        if "min_clicks" in segment_filter:
            min_clicks = segment_filter["min_clicks"]
            subscribers = [s for s in subscribers if s.total_clicks >= min_clicks]
        
        return subscribers
    
    def list_subscribers(
        self,
        status: Optional[SubscriberStatus] = None,
        tags: Optional[List[str]] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Subscriber]:
        """List subscribers with optional filtering"""
        subscribers = list(self.subscribers.values())
        
        if status:
            subscribers = [s for s in subscribers if s.status == status]
        
        if tags:
            subscribers = [
                s for s in subscribers
                if any(tag in s.tags for tag in tags)
            ]
        
        # Apply pagination
        if limit:
            subscribers = subscribers[offset:offset + limit]
        else:
            subscribers = subscribers[offset:]
        
        return subscribers
    
    def get_subscriber_count(self, status: Optional[SubscriberStatus] = None) -> int:
        """Get count of subscribers"""
        if status:
            return sum(1 for s in self.subscribers.values() if s.status == status)
        return len(self.subscribers)
    
    def bulk_import(self, subscribers_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bulk import subscribers"""
        results = {
            "total": len(subscribers_data),
            "imported": 0,
            "skipped": 0,
            "errors": []
        }
        
        for data in subscribers_data:
            try:
                subscriber = Subscriber(**data)
                self.add_subscriber(subscriber)
                results["imported"] += 1
            except Exception as e:
                results["skipped"] += 1
                results["errors"].append({
                    "email": data.get("email"),
                    "error": str(e)
                })
        
        return results
