
from . import identicon
import random
import os
from django.conf import settings
from io import BytesIO
import base64
from PIL import Image


def image_to_base64(image: Image.Image, fmt='png') -> str:
    output_buffer = BytesIO()
    image.save(output_buffer, format=fmt)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return f'data:image/{fmt};base64,' + base64_str

# def gen_identicon():
#     code = random.randint(1, 100000000000)
#     img = identicon.render_identicon(code, 16)
#     base64_str=image_to_base64(img,fmt='png')
#     return base64_str


def gen_identicon(user):
    code = random.randint(1, 100000000000)
    img = identicon.render_identicon(code, 16)
    if os.path.exists(settings.MEDIA_ROOT+"/%s"%(user.pk)):
        res = os.path.join(settings.MEDIA_ROOT, "%s" % user.pk, '%s_%s.png' % (code, 16))
        img.save(res)
        url = '%s/%s_%s.png' % (user.pk, code, 16)
        return url
    else:
        os.mkdir(settings.MEDIA_ROOT+"/%s"%(user.pk))

        res=os.path.join(settings.MEDIA_ROOT, "%s" %user.pk, '%s_%s.png' % (code, 16))
        img.save(res)
        url = '%s/%s_%s.png' % (user.pk,code, 16)
        return url


