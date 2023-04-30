from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

class Handle404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return JsonResponse({'error': 'Resource Not found'}, status=404)
        return response
