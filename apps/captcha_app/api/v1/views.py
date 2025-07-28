from rest_captcha.settings import api_settings as settings
from rest_framework import views
import uuid
from rest_captcha import utils
import base64
from rest_framework import response
from .utils import (
    random_char_challenge,
    generate_image
)
from django.core.cache import cache


class CustomizeRestCaptchaView(views.APIView):
    """
    overriding RestCaptchaView to generate captcha image
    """
    authentication_classes = ()  # noqa
    permission_classes = ()

    def post(self, request):
        key = str(uuid.uuid4())
        value = random_char_challenge(settings.CAPTCHA_LENGTH)
        cache_key = utils.get_cache_key(key)
        cache.set(cache_key, value, settings.CAPTCHA_TIMEOUT)

        # generate image
        image_bytes = generate_image(value)
        image_b64 = base64.b64encode(image_bytes)
        # print(int(value))

        data = {
            settings.CAPTCHA_KEY: key,
            settings.CAPTCHA_IMAGE: image_b64,
            'image_type': 'image/png',
            'image_decode': 'base64',
            # "captcha_num": int(value),
        }
        return response.Response(data)
