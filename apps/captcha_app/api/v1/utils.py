from rest_captcha.settings import api_settings as settings
from PIL import ImageFont, ImageDraw, Image
from .serializers import noise_default
from django.core.cache import caches
from io import BytesIO as StringIO
from rest_captcha import captcha
import os.path
import random

cache = caches[settings.CAPTCHA_CACHE]

path = os.path.dirname(__file__) + '/'  # noqa


def random_char_challenge(length):
    """
    generate random captcha code
    """
    chars = '123456789'
    ret = ''
    for i in range(length):
        ret += random.choice(chars)
    return ret.upper()


def generate_image(word):
    """
    generate captcha image
    """
    font = ImageFont.load_default()
    size = settings.CAPTCHA_IMAGE_SIZE

    xpos = 2
    from_top = 4

    image = captcha.makeimg(size)

    for char in word:
        fgimage = Image.new('RGB', size, settings.CAPTCHA_FOREGROUND_COLOR)
        charimage = Image.new('L', captcha.getsize(font, ' %s ' % char), '#000000')
        chardraw = ImageDraw.Draw(charimage)
        chardraw.text((0, 0), char, font=font, fill='#ffffff')

        charimage = charimage.crop(charimage.getbbox())
        maskimage = Image.new('L', size)

        xpos2 = xpos + charimage.size[0]
        from_top2 = from_top + charimage.size[1]
        maskimage.paste(charimage, (xpos, from_top, xpos2, from_top2))
        size = maskimage.size
        image = Image.composite(fgimage, image, maskimage)
        xpos = xpos + 2 + charimage.size[0]

    if settings.CAPTCHA_IMAGE_SIZE:
        # centering captcha on the image
        tmpimg = captcha.makeimg(size)
        xpos2 = int((size[0] - xpos) / 2)
        from_top2 = int((size[1] - charimage.size[1]) / 2 - from_top)
        tmpimg.paste(image, (xpos2, from_top2))
        image = tmpimg.crop((0, 0, size[0], size[1]))
    else:
        image = image.crop((0, 0, xpos + 1, size[1]))

    draw = ImageDraw.Draw(image)

    # settings.FILTER_FUNCTION(image)
    noise_default(image, draw)

    out = StringIO()
    image.save(out, 'PNG')
    # image.save('ss.png', 'PNG')
    content = out.getvalue()
    out.seek(0)
    out.close()

    return content
