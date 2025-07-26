from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status


class CaptchaFailed(APIException):
    """
    raised exception when user entered wrong captcha code
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('Wrong Captcha')
    default_code = 'wrong captcha'
