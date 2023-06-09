
from datetime import date
from django.contrib.auth import authenticate
from api.models import PricingPlan, Subscription, TokenUsage, User
from decouple import config
import random
from rest_framework.exceptions import AuthenticationFailed


def register_social_user(provider, user_id, email, display_name, pricing_plan, photo_url, is_verified):
    try:
        registered_user = User.objects.get(email=email)
        if (provider == registered_user.auth_provider) and is_verified:
            #If we authenticaetd user from the google lib we dont need again
            # authenticated_user = authenticate(username=email, password=config('SOCIAL_SECRET'))
            # Return to the serializer
            return {
                'id': registered_user.id,
                'username': registered_user.email,
                'display_name': registered_user.display_name,
                'photo_url': registered_user.photo_url, 
                'email': registered_user.email,
                'pricing_plan': registered_user.pricing_plan,
                'token': registered_user.token
            }

        raise AuthenticationFailed(detail='Please continue your login using ' + registered_user.auth_provider)

    except User.DoesNotExist:
        password=config('SOCIAL_SECRET')
        user = User.objects.create_user(
            email=email,
            password=password,
            pricing_plan=pricing_plan,
            display_name=display_name,
            photo_url=photo_url,
            uid=user_id,
            auth_provider=provider,
            is_verified=True
        )
        
        authenticated_user = authenticate(username=email, password=user.password)
        
        return {
                'id': authenticated_user.uid,
                'username': authenticated_user.email,
                'is_verified': authenticated_user.is_verified,
                'display_name': authenticated_user.display_name,
                'photo_url': authenticated_user.photo_url, 
                'email': authenticated_user.email,
                'pricing_plan': authenticated_user.pricing_plan,
                'token': authenticated_user.token
        }
