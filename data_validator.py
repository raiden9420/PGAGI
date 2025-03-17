import re

def validate_email(email: str) -> bool:
    """
    Validate email format using regex pattern.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.
    Accepts formats:
    - +1-234-567-8900
    - 1234567890
    - (123) 456-7890
    """
    # Remove all non-numeric characters
    cleaned = re.sub(r'\D', '', phone)
    # Check if the resulting number is 10-15 digits
    return 10 <= len(cleaned) <= 15
