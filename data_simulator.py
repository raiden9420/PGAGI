
import random
import string
from typing import Dict, List, Any

class DataSimulator:
    @staticmethod
    def generate_fake_name() -> str:
        first_names = ["Alex", "Sam", "Jordan", "Taylor", "Morgan", "Casey", "Drew", "Pat"]
        last_names = ["Smith", "Johnson", "Brown", "Davis", "Wilson", "Moore", "Taylor"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    @staticmethod
    def generate_fake_email(name: str) -> str:
        domains = ["example.com", "test.com", "demo.net"]
        email_name = name.lower().replace(" ", ".")
        return f"{email_name}@{random.choice(domains)}"

    @staticmethod
    def generate_fake_phone() -> str:
        return f"+1-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"

    @staticmethod
    def anonymize_data(data: Dict[str, Any], is_admin: bool = False) -> Dict[str, Any]:
        """Anonymize sensitive data while preserving analysis results"""
        if is_admin:
            return data  # Admins see actual data
            
        anonymized = data.copy()
        if 'name' in anonymized:
            anonymized['name'] = f"Candidate_{hash(anonymized['name'])%10000:04d}"
        if 'email' in anonymized:
            anonymized['email'] = f"candidate{hash(anonymized['email'])%10000:04d}@anonymous.com"
        if 'phone' in anonymized:
            anonymized['phone'] = f"+X-XXX-XXX-{hash(anonymized['phone'])%10000:04d}"
        return anonymized
