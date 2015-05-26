import re
from rest_framework import pagination
from rest_framework.response import Response


class CustomCursorPagination(pagination.CursorPagination):
    def get_paginated_response(self, data):
        extract_cursor_regexp = self.cursor_query_param + r'=(\w*?)(?:$|%3D)'
        next_link, prev_link = self.get_next_link(), self.get_previous_link()
        next_cursor, prev_cursor = None, None

        if next_link:
            next_cursor = re.search(extract_cursor_regexp, next_link).group(1)

        if prev_link:
            prev_cursor = re.search(extract_cursor_regexp, prev_link).group(1)

        return Response({
            'next': next_cursor,
            'previous': prev_cursor,
            'results': data
        })