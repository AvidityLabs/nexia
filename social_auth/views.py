from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from .serializers import SocialAuthSerializer



class SocialAuthView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"

        Send an idtoken as from google to get user information

        """
        payload = {
            "auth_token": request.data.get('auth_token'),
            "pricing_plan": request.data.get('pricing_plan')
        }
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        # data = ((serializer.validated_data)['auth_token'])
        return Response(serializer.data, status=status.HTTP_200_OK)