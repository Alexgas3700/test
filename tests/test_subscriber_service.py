"""Tests for subscriber service"""

import pytest
from src.models.subscriber import Subscriber, SubscriberStatus
from src.services.subscriber_service import SubscriberService


def test_add_subscriber():
    """Test adding a subscriber"""
    service = SubscriberService()
    
    subscriber = Subscriber(
        email="test@example.com",
        first_name="Test",
        last_name="User"
    )
    
    result = service.add_subscriber(subscriber)
    assert result.id == subscriber.id
    assert result.email == "test@example.com"


def test_duplicate_email():
    """Test that duplicate emails are rejected"""
    service = SubscriberService()
    
    subscriber1 = Subscriber(email="test@example.com", first_name="Test")
    service.add_subscriber(subscriber1)
    
    subscriber2 = Subscriber(email="test@example.com", first_name="Test2")
    
    with pytest.raises(ValueError):
        service.add_subscriber(subscriber2)


def test_get_subscriber_by_email():
    """Test getting subscriber by email"""
    service = SubscriberService()
    
    subscriber = Subscriber(email="test@example.com", first_name="Test")
    service.add_subscriber(subscriber)
    
    result = service.get_subscriber_by_email("test@example.com")
    assert result is not None
    assert result.email == "test@example.com"


def test_unsubscribe():
    """Test unsubscribing a subscriber"""
    service = SubscriberService()
    
    subscriber = Subscriber(email="test@example.com", first_name="Test")
    service.add_subscriber(subscriber)
    
    result = service.unsubscribe(subscriber.id, reason="Not interested")
    assert result.status == SubscriberStatus.UNSUBSCRIBED
    assert result.unsubscribed_at is not None


def test_add_tags():
    """Test adding tags to subscriber"""
    service = SubscriberService()
    
    subscriber = Subscriber(email="test@example.com", first_name="Test")
    service.add_subscriber(subscriber)
    
    result = service.add_tags(subscriber.id, ["premium", "active"])
    assert "premium" in result.tags
    assert "active" in result.tags


def test_segmentation():
    """Test subscriber segmentation"""
    service = SubscriberService()
    
    # Add subscribers with different tags
    sub1 = Subscriber(email="user1@example.com", first_name="User1", tags=["premium", "active"])
    sub2 = Subscriber(email="user2@example.com", first_name="User2", tags=["active"])
    sub3 = Subscriber(email="user3@example.com", first_name="User3", tags=["premium"])
    
    service.add_subscriber(sub1)
    service.add_subscriber(sub2)
    service.add_subscriber(sub3)
    
    # Get premium subscribers
    premium = service.get_subscribers_by_segment({"tags": ["premium"]})
    assert len(premium) == 2
    
    # Get active subscribers
    active = service.get_subscribers_by_segment({"tags": ["active"]})
    assert len(active) == 2
