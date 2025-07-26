from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class TokenBlackListedException(APIException):
    """ exception for blocked access tokens """

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('unauthorized')
    default_code = 'unauthorized'
