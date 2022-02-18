
import jwt
import uuid
import warnings

from django.contrib.auth import get_user_model

from calendar import timegm
from datetime import datetime

from rest_framework_jwt.compat import get_username
from rest_framework_jwt.compat import get_username_field
from rest_framework_jwt.settings import api_settings
from user.models import UserInfo
from django.conf import settings
import json
def jwt_payload_handler(user,request):
    username_field = get_username_field()
    username = get_username(user)
    icon_field = "icon"
    nickname_field = "nickname"
    intro_field = "intro"

    warnings.warn(
        'The following fields will be removed in the future: '
        '`email` and `user_id`. ',
        DeprecationWarning
    )
    nickname = user.nickname
    intro = user.intro


    payload = {
        'user_id': user.pk,
        'username': username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'icon':"%s"%user.icon,
        'nickname':"%s"%nickname,
        'intro':"%s"%intro
    }
    if hasattr(user, 'email'):
        payload['email'] = user.email
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    payload[username_field] = username
    payload[icon_field] = '%s://%s%s%s' % (request.scheme,request.META['HTTP_HOST'], settings.MEDIA_URL, user.icon)
    payload[nickname_field] = "%s"%nickname
    payload[intro_field] = "%s"%intro

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload




