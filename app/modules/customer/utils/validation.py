import re


def validate_email(email):
    if not email:
        return False
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email.strip()))

def validate_phone(phone):
    if not phone:
        return False
    clean_phone = phone.replace(".", "").replace("-", "").replace(" ", "")
    phone_regex = r'^(0|84|\+84)(3|5|7|8|9|1[2689])([0-9]{8})$'
    return bool(re.match(phone_regex, clean_phone))