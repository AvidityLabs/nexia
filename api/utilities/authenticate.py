from typing import Any, Optional
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

UserModel = get_user_model()

def get_user(email, password):
    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        return None

    if check_password(password, user.password):
        return user

    return None

