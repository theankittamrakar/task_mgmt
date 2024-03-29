from rest_framework import pagination, views
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import exception_handler, APIView
from rest_framework import permissions
from task_app.permissions import IsMember, IsManager


def custom_exception_handler(exc, context):
    # Call the default exception handler first
    response = exception_handler(exc, context)
    response.data['status_code'] = response.status_code
    # response.data['message'] = response.data['detail']
    # Check if the default handler was able to handle the exception
    if response.status_code == 401 or 402 or 403 or 404:
        response.data = {'status': 'False', 'detail': 'CUSTOM ERROR MESSAGE'}

    return response


#   Custom Exception Handling

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class PaginationMixin(APIView):
    pagination_class = StandardResultsSetPagination

class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

class PermissionMixin(APIView):
    def get_permissions(self):
        if hasattr(self, 'request') and self.request.method == 'GET':
            return [IsMember()]
        elif hasattr(self, 'request') and self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsManager()]
        return []