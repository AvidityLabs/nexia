from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from usecases.data import use_cases
from usecases.utils.usecase_utils import bulk_insert_use_cases

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import EmailGenerationSerializer  # Create a serializer to validate the payload
from rest_framework import permissions

from usecases.prompts.email import (
    generateEmail
)


class BulkInsertUsecases(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        
        bulk_insert_use_cases(use_cases)
        
        return Response('created',status=200)
    
    
    

class GenerateEmailView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow any user to access this view
    def post(self, request):
        # Use a serializer to validate the payload
        serializer = EmailGenerationSerializer(data=request.data)
        if serializer.is_valid():
            payload = serializer.validated_data
            email_response = generateEmail(payload)  # Call your email generation function

            # Return the email response 
            return Response(data=email_response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)