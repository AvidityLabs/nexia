import re
from rest_framework.response import Response
from rest_framework import status

def validate_text_input(text, min_length=1, max_length=2048):
    if text=="":
          return False, "Text cannot be empty"
    if not text:
        return False, "Text cannot be empty"
    elif text.isspace():
        return False, "Text cannot contain only spaces"
    elif len(text) > max_length:
        return False, "Text is too long"
    elif len(text) < min_length:
        return False, "Text is too short"
    elif text.isdigit():
        return False, "Text cannot contain only digits"
    elif all(char in "!@#$%^&*()_+-=[]{}\\|;:'\",.<>/?`~" for char in text):
        return False, "Text cannot contain only special characters"
    elif not all(ord(char) < 128 for char in text):
        return False, "Text cannot contain non-ASCII characters"
    else:
        return True, ""

def validate_email(email, password, users):
    is_valid, error = validate_text_input(email)
    if not is_valid:
        return is_valid, error

    # Check email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Invalid email format"

    # Check password length
    if len(password) < 8:
        return False, "Password is too short"

    # Check for duplicate email
    if email in users:
        return False, "Email already exists"

    return True, ""
