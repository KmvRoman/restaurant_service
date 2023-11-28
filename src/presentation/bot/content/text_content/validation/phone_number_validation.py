import re


def validate_phone_number(phone: str) -> bool:
    pattern = r'^\+998\d{9}$'
    if re.match(pattern, phone):
        return True
    else:
        return False
