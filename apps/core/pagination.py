from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20  # default
    page_size_query_param = 'page_size'  # set from client
    max_page_size = 100  # maximum items to show
