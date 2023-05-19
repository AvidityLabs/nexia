
from datetime import date
from django.contrib.auth import authenticate
from api.models import PricingPlan, Subscription, TokenUsage, User
import os
import random
from rest_framework.exceptions import AuthenticationFailed


def register_social_user(provider, user_id, email, display_name, pricing_plan, photo_url, is_verified):
    try:
        registered_user = User.objects.get(email=email)

        if provider == registered_user.auth_provider:
            authenticated_user = authenticate(email=email, password=os.environ.get('SOCIAL_SECRET'))
            return {
                'username': authenticated_user.username,
                'email': authenticated_user.email,
                'pricing_plan': authenticated_user.pricing_plan,
                'tokens': authenticated_user.token()
            }

        raise AuthenticationFailed(detail='Please continue your login using ' + registered_user.auth_provider)

    except User.DoesNotExist:
        password=os.environ.get('SOCIAL_SECRET')
        user = User.objects.create_user(
            email=email,
            password=password,
            pricing_plan=pricing_plan,
            display_name=display_name,
            photo_url=photo_url,
            uid=user_id,
            auth_provider=provider
        )
        authenticated_user = authenticate(email=email, password=user.password)
        return {
            'email': authenticated_user.email,
            'username': authenticated_user.username,
            'pricing_plan': authenticated_user.pricing_plan,
            'tokens': authenticated_user.token()
        }
