from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from usecases.data import use_cases
from usecases.utils.usecase_utils import bulk_insert_use_cases


class BulkInsertUsecases(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        
        bulk_insert_use_cases(use_cases)
        
        return Response('created',status=200)