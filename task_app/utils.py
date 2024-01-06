from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call the default exception handler first
    response = exception_handler(exc, context)
    response.data['status_code'] = response.status_code
    # response.data['message'] = response.data['detail']
    # Check if the default handler was able to handle the exception
    if response.status_code == 401 or 402 or 403 or 404:
        response.data = {'status': 'False', 'detail': 'CUSTOM ERROR MESSAGE'}

    return response
