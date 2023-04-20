import requests
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import User



class RapidAPIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Get the user's RapidAPI key from the request header
        rapid_api_key = request.META.get('X_RAPID_API_KEY', None)
        print(request.META)
        if not rapid_api_key:
            raise AuthenticationFailed('RapidAPI key not found in request headers')

        # Retrieve the user object
        try:
            user = User.objects.get(username=rapid_api_key)
        except User.DoesNotExist:
            # Create a new user if the user does not exist
            user = User.objects.create_user(
                username=rapid_api_key,
                email=f'{rapid_api_key}@nexia.user',
                is_developer=True,
                api_key=rapid_api_key
            )
        return (user, None)

        