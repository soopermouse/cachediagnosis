# cachemed/utils/formatters.py
from datetime import datetime

def format_date(timestamp, format='%Y-%m-%d'):
    """Format timestamp to date string"""
    if not timestamp:
        return None
    return datetime.fromtimestamp(timestamp).strftime(format)

def format_datetime(timestamp, format='%Y-%m-%d %H:%M:%S'):
    """Format timestamp to datetime string"""
    if not timestamp:
        return None
    return datetime.fromtimestamp(timestamp).strftime(format)

def format_bytes(bytes):
    """Format bytes to human readable"""
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1024**2:
        return f"{bytes/1024:.1f} KB"
    elif bytes < 1024**3:
        return f"{bytes/1024**2:.1f} MB"
    else:
        return f"{bytes/1024**3:.1f} GB"