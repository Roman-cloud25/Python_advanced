from rest_framework.pagination import CursorPagination

# Safe pagination
class SecureCursorPagination(CursorPagination):
    # Disable page resizing
    page_size_query_param = None
    max_page_size = None
    ordering = '-created_at'
    cursor_query_param = 'cursor'
