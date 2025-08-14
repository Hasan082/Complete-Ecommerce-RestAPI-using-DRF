from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

class StandardResultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'count': self.page.paginator.count,
                'current_page': self.page.number,
                'total_pages': math.ceil(self.page.paginator.count / self.page_size),
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'results': data
        })