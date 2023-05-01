import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

def decode_jwt_token(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if auth_header:
        try:
            auth_token = auth_header.split(' ')[1]
            decoded_token = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except IndexError:
            raise AuthenticationFailed('Token prefix missing')
        except Exception:
            raise AuthenticationFailed('Token is invalid')
    else:
        raise AuthenticationFailed('Authorization header missing')