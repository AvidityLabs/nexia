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
        print('incomming request------------')
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # data = ((serializer.validated_data)['auth_token'])
        return Response(serializer.data, status=status.HTTP_200_OK)