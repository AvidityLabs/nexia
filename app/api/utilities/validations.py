from api.models import User

def check_duplicate_email(email):
    try:
        User.objects.get(email=email)
        payload = {'is_valid': False, 'error': 'Email already exists'}
    except User.DoesNotExist:
        payload = {'is_valid': True, 'error': ''}
    return payload




