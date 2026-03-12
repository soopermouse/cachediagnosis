# cachemed/utils/validators.py
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """Validate phone number (simple)"""
    pattern = r'^\+?[\d\s-]{10,}$'
    return bool(re.match(pattern, phone))

def validate_date(date_str):
    """Validate ISO date format"""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, date_str))