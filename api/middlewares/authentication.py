import requests
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import User

class RapidAPIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Get the user's RapidAPI key from the request header
        rapid_api_key = request.META.get('X-RapidAPI-Key', None)
        print(rapid_api_key)
        if not rapid_api_key:
            raise AuthenticationFailed('RapidAPI key not found in request headers')

        # Make a request to RapidAPI to obtain the user's information
        url = 'https://rapidapi.com/user'
        headers = {'X-RapidAPI-Key': rapid_api_key}
        response = requests.get(url, headers=headers)

        # Extract the user's information from the response
        if response.status_code == 200:
            user_info = response.json()
            username = user_info.get('username', '')
            email = user_info.get('email', '')
            user = User.objects.get_or_create(username=username, email=email)
            return (user, None)
        else:
            raise AuthenticationFailed('Invalid RapidAPI key')
        