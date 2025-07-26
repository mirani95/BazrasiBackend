"""
    You should probably add a custom exception handler to your project based on
    who consumes your APIs. To learn how to create a custom exception handler,
    you can check out the Django Rest Framework documentation at:
    https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling
"""

from rest_framework.exceptions import APIException
from rest_framework import status


class ConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Object already exists."
    default_code = "conflict"
