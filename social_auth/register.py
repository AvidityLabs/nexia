
from datetime import date
from django.contrib.auth import authenticate
from api.models import PricingPlan, Subscription, TokenUsage, User
import os
import random
from rest_framework.exceptions import AuthenticationFailed


def register_social_user(provider, user_id, email, display_name, pricing_plan, photo_url, is_verified):
    try:
        registered_user = User.objects.get(email=email)
        print(registered_user)

        if provider == registered_user.auth_provider:
            authenticated_user = authenticate(username=email, password=os.environ.get('SOCIAL_SECRET'))
            # Return to the serializer
            return {
                'id': authenticated_user.id,
                'username': authenticated_user.email,
                'display_name': authenticated_user.display_name,
                'photo_url': authenticated_user.photo_url, 
                'email': authenticated_user.email,
                'pricing_plan': authenticated_user.pricing_plan,
                'auth_token': authenticated_user.token
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
            is_verified=True,
            auth_provider=provider
        )
        
        authenticated_user = authenticate(username=email, password=user.password)
        
        return {
                'id': authenticated_user.uid,
                'username': authenticated_user.email,
                'display_name': authenticated_user.display_name,
                'photo_url': authenticated_user.photo_url, 
                'email': authenticated_user.email,
                'pricing_plan': authenticated_user.pricing_plan,
                'auth_token': authenticated_user.token
        }
