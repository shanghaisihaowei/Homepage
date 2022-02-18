from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
# from rest_framework_jwt.utils import jwt_decode_handler
from user import models
import jwt
# from rest_framework.authentication import get_authorization_header
# from rest_framework_jwt.settings import api_settings

# class MyJSONWebTokenAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         jwt_value = get_authorization_header(request)
#         if not jwt_value:
#             raise exceptions.AuthenticationFailed('未登录，没有Token')
#         try:
#             payload = jwt_decode_handler(jwt_value)
#         except jwt.ExpiredSignature:
#             raise exceptions.AuthenticationFailed('签名过期')
#         except jwt.InvalidTokenError:
#             print('非法用户')
#             raise exceptions.AuthenticationFailed('非法用户')
#         user = models.UserInfo.objects.filter(pk=payload['user_id']).first()
#         return user, jwt_value


# 普通认证(可以要用户登录也可以不用)
class GeneralAuthentication(BaseAuthentication):
    def authenticate(self, request):
        jwt_value = get_authorization_header(request)
        # 如果没有获取到token(即未登录状态)
        if not jwt_value:
            return None
        # payload = jwt_decode_handler(jwt_value)
        # user = models.UserInfo.objects.filter(pk=payload['user_id']).first()
        # 判断token是否正确
        if not user:
            return None
        return user, jwt_value




from django.conf import settings


from jwt import decode as jwt_decode
from jwt import encode as jwt_encode
from jwt.exceptions import ExpiredSignatureError
class JwtAuth:

    def __init__(self):
        self.key = settings.SECRET_KEY
        self.result = {"status": 404, "msg": "token校验失败", "token": None, "payload": None}
        self.HTTP_HEADER_ENCODING = 'iso-8859-1'
    def generate_jwt_token(self, payload):
        token = jwt_encode(payload=payload, key=self.key, algorithm='HS256')
        # print(token)
        self.result['status'] = 200
        self.result['msg'] = "校验成功"
        self.result['token'] = token
        return self.result

    def get_authorization(self,token):
        """
        Return request's 'Authorization:' header, as a bytestring.

        Hide some test client ickyness where the header can be unicode.
        """
        if isinstance(token, str):
            # Work around django test client oddness
            token = token.encode(self.HTTP_HEADER_ENCODING)
            print(token,5555)
        return token

    def check_jwt_token(self, token):
        # token=self.get_authorization(token)
        try:
            # payload = jwt_decode_handler(token)
            payload = jwt_decode(token, key=self.key, algorithms=["HS256"])
            self.result['status'] = 200
            self.result['msg'] = "校验成功"
            self.result['token'] = token
            self.result['payload'] = payload
        except jwt.ExpiredSignatureError:
            self.result['msg'] = "token过期"
            return self.result
        except jwt.DecodeError:
            self.result['msg'] = "token认证失败"
        except jwt.InvalidTokenError:
            self.result['msg'] = "token非法"
        finally:
            return self.result

