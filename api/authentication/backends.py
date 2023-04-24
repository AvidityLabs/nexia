import os
import jwt

from django.conf import settings

from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed

from api.models import User
from api.utilities.subscription import update_subscription

RAPID_API_APP_URL =  os.environ.get('RAPID_API_APP_URL')
HTTP_X_RAPIDAPI_PROXY_SECRET = os.environ.get('HTTP_X_RAPIDAPI_PROXY_SECRET')
SECRET_KEY = os.environ.get('SECRET_KEY')

class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        """
        The `authenticate` method is called on every request regardless of
        whether the endpoint requires authentication. 

        `authenticate` has two possible return values:

        1) `None` - We return `None` if we do not wish to authenticate. Usually
                    this means we know authentication will fail. An example of
                    this is when the request does not include a token in the
                    headers.

        2) `(user, token)` - We return a user/token combination when 
                             authentication is successful.

                            If neither case is met, that means there's an error 
                            and we do not return anything.
                            We simple raise the `AuthenticationFailed` 
                            exception and let Django REST Framework
                            handle the rest.
        """
        request.user = None
        # print('\033[32m' + 'start' + '\033[0m')
        # `auth_header` should be an array with two elements: 1) the name of
        # the authentication header (in this case, "Token") and 2) the JWT 
        # that we should authenticate against.
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
        rapidapi_host = request.META.get('X_RAPID_API_HOST')
       

        if not rapidapi_host:
            raise AuthenticationFailed('X-RapidAPI-Host not found in request headers')
        

        if not auth_header:
            return None
        
        
        if len(auth_header) == 1:
            # Invalid token header. No credentials provided. Do not attempt to authenticate.

            return None

        elif len(auth_header) > 2:
            # Invalid token header. The Token string should not contain spaces. Do
            # not attempt to authenticate.
            return None

        # The JWT library we're using can't handle the `byte` type, which is
        # commonly used by standard libraries in Python 3. To get around this,
        # we simply have to decode `prefix` and `token`. This does not make for
        # clean code, but it is a good decision because we would get an error
        # if we didn't decode these values.
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')
        prefix = auth_header[0].decode('utf-8') if isinstance(auth_header[0], bytes) else auth_header[0]
        token = auth_header[1].decode('utf-8') if isinstance(auth_header[1], bytes) else auth_header[1]

        if prefix.lower() != auth_header_prefix:
            # The auth header prefix is not what we expected. Do not attempt to
            # authenticate.
            return None

        # By now, we are sure there is a *chance* that authentication will
        # succeed. We delegate the actual credentials authentication to the
        # method below.
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Try to authenticate the given credentials. If authentication is
        successful, return the user and token. If not, throw an error.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except Exception as e:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed()

        try:
            user = User.objects.get(pk=payload['id'])
            update_subscription(user, request)
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)
        
        return (user, token)
    