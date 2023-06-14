from django.http import JsonResponse

class InternalServerErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 500:
            error_message = "An internal server error occurred. Please try again later. If the problem persists, please contact the API owner for assistance."
            return JsonResponse({'error': error_message, "status_code": 500}, status=500)

        return response
