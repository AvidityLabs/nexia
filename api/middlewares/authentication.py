import os
import requests
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import User, PricingPlan, Subscription


HTTP_X_RAPIDAPI_PROXY_SECRET = os.environ.get('HTTP_X_RAPIDAPI_PROXY_SECRET')
APP_URL = 'https://rapidapi.com/AvidityLabs/api/nexia2'

def get_subscription(request):
    plan = request.META.get('HTTP_X_RAPIDAPI_SUBSCRIPTION')
    pricing_plan, created = PricingPlan.objects.get_or_create(name=plan)
    if created:
        subscription = Subscription.objects.create(pricing_plan=pricing_plan)
    else:
        subscription = Subscription.objects.get(pricing_plan=pricing_plan)
    return subscription


class RapidAPIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        print(request.META)
        if request.META.get('PATH_INFO') == '/api/register/' or request.META.get('PATH_INFO') == '/api/get_token/':
            # Skip authentication for registration endpoint
            return None
        else:
            # Get the user's RapidAPI key from the request header
            authorization_key = request.META.get('HTTP_AUTHORIZATION', None)
            rapid_api_host = request.META.get('HTTP_X_RAPIDAPI_HOST', None)
            rapid_api_proxy_secret = request.META.get('HTTP_X_RAPIDAPI_PROXY_SECRET', None)

            if not authorization_key:
                raise AuthenticationFailed('Authorization key not found in request headers. Go to /register endpoint to get access key.')
            if rapid_api_host:
                raise AuthenticationFailed('RapidAPI Host not found in request headers')
            if rapid_api_proxy_secret != HTTP_X_RAPIDAPI_PROXY_SECRET:
                raise AuthenticationFailed(f'Invalid RapidAPI Proxy Secret. This API can only be accessed through the RapidAPI platform. Please sign up for RapidAPI and use their platform to access this API.{APP_URL}')

            # Retrieve the user object
            try:
                user = User.objects.get(developer_id=authorization_key)
                # Add subscription
                subscription = get_subscription(request)
                if user.subscription != subscription:
                    user.subscription = subscription
                    user.save()
                return (user, None)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not registered with this API. Please sign up for RapidAPI and use their platform to access this API.')


        

        