from django.shortcuts import render

# Create your views here.

from utils.APIResponse import APIResponse
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from .models import UserInfo
from rest_framework.exceptions import APIException
import re

from django.conf import settings
from .serializers import RegisterSerializer
from .serializers import LoginSerilizers
from .serializers import PutPwdSerilizers
from .serializers import CodeLoginSerilizers
from utils import HomePage_logging
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserDetailModelSerializer
from .serializers import UserDetailUpdateModelSerializer
from .serializers import PasswordPutModelSerializer
from .serializers import AuthenticationPostModelSerializer
logger = HomePage_logging.get_logger()
from celery_task.user_task import send_code_message
from django.core.cache import cache
from django.conf import settings
from .files import FileRenderCN, FileRenderEN
from .models import Authentication_tab
from rest_framework.response import Response
import base64
import uuid
import os
from PIL import Image
class EmailViewSet(ViewSet):
    """
    GET:
        get_email：邮箱是否存在

    GET:
        re_codes：注册获取邮箱验证

    GET:
        login_codes：登录获取邮箱验证码

    GET:
        pwd_codes：修改密码获取邮箱验证
    """
    authentication_classes = []
    permission_classes = []
    def get_lang(self):
        lang = self.request.META.get('HTTP_LANGUAGE')

        if lang:
            if lang == 'zh-hans':
                return lang
            else:
                return lang
        else:
            return 'en-US'

    @action(methods='GET', detail=False)
    def get_email(self, request, *args, **kwargs):
        """
        查看邮箱是否注册
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        email = request.query_params.get('email')
        print(email)
        if not re.match(r"^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$", email):
            raise APIException({"detail": "The email number is invalid"})
        email_obj = UserInfo.objects.filter(email=email).first()
        if email_obj:
            return APIResponse(code=4001, msg='邮箱已注册')
        else:
            return APIResponse(code=200, msg='邮箱可以注册')

    @action(methods='GET', detail=False)
    def reg_codes(self, request, *args, **kwargs):
        """
        获取注册验证码
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        email = request.query_params.get('email')
        if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$', email):
            raise APIException({"detail": "The email number is invalid"})
        lang=self.get_lang()
        send_code_message.delay(settings.CACHE_REG_SMS, "注册验证码", email, 1,lang)
        return APIResponse(code=200, result=[])


    @action(methods='GET', detail=False)
    def login_codes(self, request, *args, **kwargs):
        """
        获取邮箱验证码
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        email = request.data.get('email')
        if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$', email):
            raise APIException({"detail": "The email number is invalid"})
        lang=self.get_lang()
        send_code_message.delay(settings.CACHE_LOGIN_SMS, "登录验证码", email, 2,lang)
        return APIResponse(code=200, result=[])


    @action(methods='GET', detail=False)
    def pwd_codes(self, request, *args, **kwargs):
        """
        获取修改密码验证码
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        email = request.query_params.get('email')
        if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$', email):
            raise APIException({"detail": "The email number is invalid"})
        lang=self.get_lang()
        send_code_message.delay(settings.CACHE_PUTPWD_SMS, "修改密码验证码", email, 3,lang)
        return APIResponse(code=200, result=[])

    @action(methods='GET', detail=False)
    def alipay_codes(self, request, *args, **kwargs):
        """
        获取修改密码验证码
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        email = request.query_params.get('email')
        if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$', email):
            raise APIException({"detail": "The email number is invalid"})
        lang=self.get_lang()
        send_code_message.delay(settings.CACHE_ACCOUNT_SMS, "添加账户验证码", email, 4,lang)
        return APIResponse(code=200, result=[])


class RegisterViewSet(ViewSet):
    """
    POST:
        reg注册接口
        参数：1、code 2、password 3、re_password

    """
    authentication_classes = []
    permission_classes = []
    def get_lang(self, data):
        lang = self.request.META.get('HTTP_LANGUAGE')

        if lang:
            if lang == 'zh-hans':
                return FileRenderCN().render(data)
            else:
                return FileRenderEN().render(data)
        else:
            return FileRenderEN().render(data)

    @action(methods='POST', detail=False)
    def reg(self, request, *args, **kwargs):
        data = self.request.data
        print(data)
        if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$', data['email']):
            raise APIException({"detail": "请输入正确的邮箱"})
        elif data['password'] != data['re_password']:
            raise APIException({"detail": "两次密码不一致！"})
        email=data['email']
        code = str(cache.get(settings.CACHE_REG_SMS % email))
        verification_code =str(data['code'])
        if code != verification_code:
            raise APIException({"detail": "验证码不正确！"})
        if not re.match(r'^[a-zA-Z0-9]{6,18}$', data['password']):
            raise APIException({"detail": "密码不能包含中文，长度6位数以上，并且包含英语与数字"})
        elif UserInfo.objects.filter(email=data['email']).first():
            raise APIException({"detail": "你已经注册过了！"})
        ser = RegisterSerializer(data=self.request.data)
        ser.is_valid()
        ser.save()
        user_obj=UserInfo.objects.filter(email=data['email']).first()
        result = {'username':user_obj.username,"password":data['password']}
        return APIResponse(code=200,result=result)






class LoginViewSet(ViewSet):
    """
    POST:
        login登录接口
        参数：1、email 2、password
    POST:
        code_login 验证码登录
        参数：1、code 2、email
    """
    def get_lang(self, data):
        lang = self.request.META.get('HTTP_LANGUAGE')

        if lang:
            if lang == 'zh-hans':
                return FileRenderCN().render(data)
            else:
                return FileRenderEN().render(data)
        else:
            return FileRenderEN().render(data)


    @action(methods='POST', detail=False)
    def login(self, request, *args, **kwargs):
        data=self.request.data
        if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$',data['email']):
            raise APIException({"detail": "请输入正确的邮箱"})
        elif not re.match(r'^[a-zA-Z0-9]{6,18}$', data['password']):
            raise APIException({"detail": "密码不能包含中文，长度6位数以上，并且包含英语与数字"})
        user_obj = UserInfo.objects.filter(email=data['email']).first()
        if user_obj is None:
            raise APIException({"detail": "用户名或密码错误"})
        else:
            if not user_obj.check_password(data['password']):
                raise APIException({"detail": "用户名或密码错误"})
            else:
                # result={"token":token}
                return APIResponse(code=200)


    @action(methods='POST', detail=False)
    def code_login(self, request, *args, **kwargs):
        ser = CodeLoginSerilizers(data=request.data, context={'request': request})
        if ser.is_valid(raise_exception=True):
            logger.warning("IP为%s 的 用户:%s 登录了" % (ser.context.get('ip'), ser.context.get('email')))
            result = [
                {'id': ser.context.get('id'), 'token': ser.context.get('token'), 'email': ser.context.get('email'),
                 'icon': ser.context.get('icon'), 'intro': ser.context.get('intro'), 'ip': ser.context.get('ip')}]
            return APIResponse(code=200, result=result)


class PutPwdViewSet(ViewSet):
    """
    put：修改密码

    json数据格式{
    "email": "329025421@qq.com",
    "code": "449921",
    "password": "012345678",
    "re_password": "012345678"
}
    """
    def get_lang(self, data):
        lang = self.request.META.get('HTTP_LANGUAGE')

        if lang:
            if lang == 'zh-hans':
                return lang
            else:
                return lang
        else:
            return 'zh-hans'
    def putpwd(self, request, *args, **kwargs):
        data = self.request.data
        if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$',data['email']):
            raise APIException({"detail": "邮箱格式不正确"})
        verification_code = data['code']
        code = cache.get(settings.CACHE_PUTPWD_SMS % data['email'])
        if code != verification_code:
            raise APIException({"detail": "验证码不正确"})
        if data['password'] != data['re_password']:
            raise APIException({"detail": "密码不一致"})
        if not re.match(r'^[a-zA-Z0-9]{6,18}$', data['password']) and not re.match(r'^[a-zA-Z0-9]{6,18}$', data['password']):
            raise APIException({"detail": "密码不能包含中文，长度6位数以上，并且包含英语与数字"})
        user = UserInfo.objects.filter(email=data['email'],is_delete=False).first()
        if user:
            user.set_password(data['password'])
            user.save()
            return APIResponse(code=200, result=[])
        else:
            raise APIException({"detail": "用户不存在"})



class PasswordPutView(GenericViewSet, UpdateModelMixin):
    """
    put:
        个人中心修改密码

    """

    queryset = UserInfo.objects.filter().all()
    serializer_class = PasswordPutModelSerializer
    authentication_classes = (JWTAuthentication, )

    def get_lang(self, data):
        lang = self.request.META.get('HTTP_LANGUAGE')

        if lang:
            if lang == 'zh-hans':
                return FileRenderCN().render(data)
            else:
                return FileRenderEN().render(data)
        else:
            return FileRenderEN().render(data)


    def update(self, request, *args, **kwargs):
        print(self.request.user.id)
        data = self.request.data
        print(data)
        if not re.match(r'^[a-zA-Z0-9]{6,18}$', data['password']) and not re.match(r'^[a-zA-Z0-9]{6,18}$', data['password']):
            raise APIException({"detail": "密码不能包含中文，长度6位数以上，并且包含英语与数字"})
        user = UserInfo.objects.filter(id=self.request.user.id).first()
        user.set_password(data['password'])
        user.save()
        result={'email':user.email}
        return APIResponse(code=200,result=result)

from HomePage.views import MyRefreshToken



class UserDetailView(GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    """
    retrieve:
        查看用户自己的信息

    update：
        更新用户自己的信息,自动签发token
    """

    queryset = UserInfo.objects.filter().all()
    serializer_class = UserDetailModelSerializer
    authentication_classes = (JWTAuthentication, )

    def get_object(self):
        return self.request.user

    def get_lang(self, data):
        lang = self.request.META.get('HTTP_LANGUAGE')

        if lang:
            if lang == 'zh-hans':
                return FileRenderCN().render(data)
            else:
                return FileRenderEN().render(data)
        else:
            return FileRenderEN().render(data)

    def get_serializer_class(self):
        if self.request.method  == 'GET':
            return UserDetailModelSerializer
        else :
            return UserDetailUpdateModelSerializer


    def retrieve(self, request, *args, **kwargs):
        serializer = super().retrieve(request, *args, **kwargs)
        result = serializer.data
        return APIResponse(result=result)

    def update(self, request, pk, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        icon=request.FILES.get('icon')
        nickname=request.data.get('nickname')
        if len(nickname)==0:
            raise APIException({"detail": "昵称不能为空"})
        if len(nickname)>20:
            raise APIException({"detail": "昵称不能超过20个字符"})
        user_dict = {
            'icon':icon,
            'nickname':request.data.get('nickname'),
            'intro':request.data.get('intro'),
        }
        serializer = self.get_serializer(instance, data=user_dict, partial=partial,context={'request':request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        user=UserInfo.objects.filter(id=request.user.pk).first()

        token_obj=MyRefreshToken()
        token=token_obj.for_user(user)
        refreshtoken =str(token.access_token)
        result = {'access':refreshtoken,'nickname':serializer.data.get('nickname'),'intro':serializer.data.get('intro'),'icon':'%s://%s%s%s' % (request.scheme,request.META['HTTP_HOST'], settings.MEDIA_URL,serializer.data.get('icons'))}
        return APIResponse(result=result)
    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

# from rest_framework.generics import GenericAPIView
# class UserDetailView(GenericAPIView):
#     queryset = UserInfo.objects.filter().all()
#     serializer_class = UserDetailModelSerializer
#     authentication_classes = (JWTAuthentication, )
#
#     def get_object(self):
#         return self.request.user
#     def get(self,request):
#         serializer  = self.get_serializer(instance=self.get_object())
#         return APIResponse(result=serializer.data)
#
#
#
# class UserDetailUpdateView(GenericAPIView):
#     queryset = UserInfo.objects.filter().all()
#     serializer_class = UserDetailUpdateModelSerializer
#     authentication_classes = (JWTAuthentication, )
#     def get_object(self):
#         return self.request.user
#
#     def put(self, request):
#         data = request.data
#         serializer = self.get_serializer(instance=self.get_object(), data=data)
#
#         serializer.is_valid(raise_exception=True)
#
#         serializer.save()
#
#         serializer = self.get_serializer(instance=self.get_object())
#         result = {"token": token,"data":serializer.data}
#         return APIResponse(result=result)

from rest_framework.mixins import CreateModelMixin,ListModelMixin
from utils.id_card_ocr import parse
class AuthenticationView(GenericViewSet,CreateModelMixin,ListModelMixin):
    queryset = Authentication_tab.objects.filter().all()
    serializer_class =AuthenticationPostModelSerializer
    authentication_classes = (JWTAuthentication, )
    def get_queryset(self):
        if self.request.user:
            return Authentication_tab.objects.filter(is_delete=False,email=self.request.user.email)
        else:
            return Authentication_tab.objects.none()


    def get_serializer_class(self):
        if self.action in ['create']:
            return AuthenticationPostModelSerializer
        elif self.action in ['list']:
            return AuthenticationPostModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        try:
            atth_obj=Authentication_tab.objects.filter(email=request.user.email,verify_status__in=[0,3],is_delete=False).first()
            atth_obj.delete()
            # atth_obj.save()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)
        except Exception:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)



class Auth_status(GenericViewSet,RetrieveModelMixin):
    queryset = Authentication_tab.objects.filter().all()
    serializer_class = AuthenticationPostModelSerializer
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        if self.request.user:
            return Authentication_tab.objects.filter(is_delete=False, email=self.request.user.email)
        else:
            return Authentication_tab.objects.none()
    def retrieve(self, request, *args, **kwargs):
        try:
            auth_obj=Authentication_tab.objects.filter(is_delete=False,email=self.request.user.email).last()
            if auth_obj.verify_status == 0:
                return APIResponse(result={"verify_status":0,'msg':'提交信息','status':False})
            elif auth_obj.verify_status == 1:
                return APIResponse(result={"verify_status": 1, 'msg': '审核中','status':False})
            elif auth_obj.verify_status == 2:
                return APIResponse(result={"verify_status": 2, 'msg': '认证完成','status':True})
            elif auth_obj.verify_status == 3:
                return APIResponse(result={"verify_status": 3, 'msg': '认证失败','status':False})
        except Exception:
            return APIResponse(result={"verify_status": 4, 'msg': '用户未实名认证','status':False})