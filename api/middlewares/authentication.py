import os
from django.db import IntegrityError
import requests
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import User
from api.utilities.subscription import get_subscription


HTTP_X_RAPIDAPI_PROXY_SECRET = os.environ.get('HTTP_X_RAPIDAPI_PROXY_SECRET')
RAPID_API_APP_URL = 'https://rapidapi.com/AvidityLabs/api/nexia2'


class RapidAPIAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        # print(request.META)
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
            if not rapid_api_host:
                raise AuthenticationFailed('RapidAPI Host not found in request headers')
            if rapid_api_proxy_secret != HTTP_X_RAPIDAPI_PROXY_SECRET:
                raise AuthenticationFailed(f'Invalid RapidAPI Proxy Secret. This API can only be accessed through the RapidAPI platform. Please sign up for RapidAPI and use their platform to access this API.{RAPID_API_APP_URL}')

            try:
                user = User.objects.get(api_key=authorization_key)
                return (user, None)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not registered with this API. Please sign up for RapidAPI and use their platform to access this API.')


        

        