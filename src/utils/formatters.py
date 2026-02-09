"""Formatting utilities"""

from datetime import datetime
from typing import Optional


def format_date(
    date: datetime,
    format_string: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """Format a datetime object"""
    return date.strftime(format_string)


def format_number(
    number: float,
    decimal_places: int = 2,
    use_comma: bool = True
) -> str:
    """Format a number with decimal places and optional comma separator"""
    formatted = f"{number:.{decimal_places}f}"
    
    if use_comma:
        parts = formatted.split(".")
        parts[0] = "{:,}".format(int(parts[0]))
        formatted = ".".join(parts)
    
    return formatted


def format_percentage(value: float, decimal_places: int = 2) -> str:
    """Format a value as a percentage"""
    return f"{value:.{decimal_places}f}%"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to a maximum length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
