from django.http import JsonResponse


class CustomExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            response = self.handle_exception(request, e)

        if response.status_code == 404:
            # Customize the JSON response for 404
            custom_response = {
                'error': 'Not Found',
                'detail': 'The requested resource was not found on this server.',
                'status_code': response.status_code
            }
            response = JsonResponse(custom_response, status=404)

        elif response.status_code == 500:
            custom_response = {
                'error': 'Internal Server Error',
                'detail': 'Something went wrong.',
                'status_code': response.status_code
            }
            response = JsonResponse(custom_response, status=500)

        elif response.status_code == 403:
            custom_response = {
                'error': 'Forbidden',
                'detail': 'You do not have permission to access the requested resource.',
                'status_code': response.status_code
            }
            response = JsonResponse(custom_response, status=403)

        elif response.status_code == 400 and hasattr(request, 'validation_errors'):
            # Check if the request has validation errors
            custom_response = {
                'error': 'Bad Request',
                'detail': 'Validation Error',
                'status_code': response.status_code,
                'validation_errors': request.validation_errors
            }
            response = JsonResponse(custom_response, status=400)

        return response

    def handle_exception(self, request, exception):
        # Your custom exception handling logic here
        # ...

        # If you want to re-raise the exception, you can do so
        raise exception
