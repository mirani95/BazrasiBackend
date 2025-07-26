from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.captcha_app import exceptions as captcha_exception
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from apps.authentication.models import User
from rest_framework import exceptions
from django.core.cache import cache
from rest_framework import status
from typing import Any


class CustomizedTokenObtainPairSerializer(TokenObtainPairSerializer):  # noqa
    """
    customize jwt token
    'set new variables in generated token'
    """

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        """
        override validate method to add more conditions
        """
        captcha_code = self.context['request'].data['captcha_code']
        captcha_key = self.context['request'].data['captcha_key']

        if captcha_code != cache.get(captcha_key) or 'captcha_code' not in self.context['request'].data.keys():
            raise captcha_exception.CaptchaFailed()

        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["otp_status"] = self.user.otp_status

        if not self.user.is_active:
            raise exceptions.APIException(
                "user is not active",
                status.HTTP_403_FORBIDDEN
            )

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

    @classmethod
    def get_token(cls, user):
        """
        set variables in encoded jwt token
        """

        token = super().get_token(user)

        # get customized user
        auth_user_model = User.objects.get(username=user.username)

        # Add custom claims
        token['name'] = user.username
        token['mobile'] = auth_user_model.mobile
        token['national_code'] = auth_user_model.national_code

        return token
