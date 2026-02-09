"""Configuration management"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """Configuration class"""
    
    def __init__(self, config_data: Dict[str, Any]):
        self.data = config_data
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        keys = key.split(".")
        value = self.data
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    @property
    def smtp(self) -> Dict[str, Any]:
        """Get SMTP configuration"""
        return self.data.get("smtp", {})
    
    @property
    def tracking(self) -> Dict[str, Any]:
        """Get tracking configuration"""
        return self.data.get("tracking", {})
    
    @property
    def rate_limiting(self) -> Dict[str, Any]:
        """Get rate limiting configuration"""
        return self.data.get("rate_limiting", {})
    
    @property
    def database(self) -> Dict[str, Any]:
        """Get database configuration"""
        return self.data.get("database", {})


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file or environment"""
    
    # Default configuration
    default_config = {
        "smtp": {
            "host": os.getenv("SMTP_HOST", "smtp.example.com"),
            "port": int(os.getenv("SMTP_PORT", "587")),
            "username": os.getenv("SMTP_USERNAME", ""),
            "password": os.getenv("SMTP_PASSWORD", ""),
            "use_tls": os.getenv("SMTP_USE_TLS", "true").lower() == "true",
            "use_ssl": os.getenv("SMTP_USE_SSL", "false").lower() == "true",
        },
        "email": {
            "default_from_email": os.getenv("DEFAULT_FROM_EMAIL", "noreply@example.com"),
            "default_from_name": os.getenv("DEFAULT_FROM_NAME", "Marketing Team"),
        },
        "tracking": {
            "enabled": True,
            "track_opens": True,
            "track_clicks": True,
            "tracking_domain": os.getenv("TRACKING_DOMAIN", "track.example.com"),
        },
        "rate_limiting": {
            "max_emails_per_hour": int(os.getenv("MAX_EMAILS_PER_HOUR", "1000")),
            "max_emails_per_day": int(os.getenv("MAX_EMAILS_PER_DAY", "10000")),
        },
        "database": {
            "url": os.getenv("DATABASE_URL", "sqlite:///marketing.db"),
        },
        "redis": {
            "host": os.getenv("REDIS_HOST", "localhost"),
            "port": int(os.getenv("REDIS_PORT", "6379")),
            "db": int(os.getenv("REDIS_DB", "0")),
        }
    }
    
    # Load from file if provided
    if config_path:
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, "r") as f:
                file_config = json.load(f)
                # Merge with defaults
                default_config.update(file_config)
    
    return Config(default_config)
