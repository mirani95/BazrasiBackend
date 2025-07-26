import random

from rest_captcha import utils
from rest_captcha.settings import api_settings
from django.core.cache import caches

cache = caches[api_settings.CAPTCHA_CACHE]


def noise_dots(draw, image, fill):
    size = image.size
    for p in range(int(size[0] * size[1] * 0.07)):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        draw.point((x, y), fill=fill)
    return draw


def noise_default(image, draw):
    draw = noise_dots(draw, image, api_settings.CAPTCHA_FOREGROUND_COLOR)
    # draw = utils.noise_arcs(draw, image, api_settings.CAPTCHA_FOREGROUND_COLOR)
