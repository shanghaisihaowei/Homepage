import json

from rest_framework import serializers
from django.core.cache import cache
from django.conf import settings
from rest_framework.exceptions import ValidationError
import re
from .models import UserInfo
from .models import Authentication_tab
from utils.HomePage_logging import get_logger

# from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from utils import get_code,get_icon
from django.core.mail import send_mail
from utils.getnickname import get_nickname
from rest_framework.exceptions import ValidationError
from django.db import transaction
import base64
import uuid
import os
from PIL import Image
logger = get_logger()
from my_wallet.models import Dollar_wallet,Rmb_wallet

class RegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        required=True,
        min_length=6,
        max_length=6,
        write_only=True,
        error_messages={"blank": "请输入验证码", "required": "请输入验证码", "max_length": "验证码格式错误", "min_length": "验证码格式错误"},
        help_text="验证码")
    password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=16,
        error_messages={"blank": "请输入密码", "required": "请输入密码", "max_length": "密码不能包含中文，长度6位数以上，并且包含英语与数字", "min_length": "密码不能包含中文，长度6位数以上，并且包含英语与数字"},
        write_only=True, )
    re_password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=16,
        error_messages={"blank": "请输入密码", "required": "请输入密码", "max_length": "密码不能包含中文，长度6位数以上，并且包含英语与数字",
                        "min_length": "密码不能包含中文，长度6位数以上，并且包含英语与数字"},
        write_only=True, )

    class Meta:
        model = UserInfo
        fields = ['code', 'email', 'password','re_password']

    def create(self, validated_data):
        print(validated_data)
        res = []
        try:
            with transaction.atomic():
                validated_data.pop('code')
                validated_data.pop('re_password')
                validated_data['username'] = validated_data['email']
                validated_data['nickname'] = get_nickname()
                validated_data['intro'] = '我的签名'
                print(validated_data)
                res = UserInfo.objects.create_user(**validated_data)
                res.save()
                user = UserInfo.objects.filter(email=validated_data['email']).first()
                url = get_icon.gen_identicon(user)
                user.icon = url
                user.save()
                Rmb_wallet.objects.create(userinfos=user)
                Dollar_wallet.objects.create(userinfos=user)
                print(validated_data.get('email') + '注册成功')
        except Exception as e:
            logger.error('注册写入数据库出现错误，错误原因是:%s' % e)
            raise ValidationError({'detail': e})
        return res


class LoginSerilizers(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'email', 'password', 'icon']
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'icon': {
                'read_only': True,
            },
            "email": {"write_only": True, 'required': True},
            "password": {"write_only": True, "max_length": 16, "min_length": 8, 'required': True}
        }

    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(user)
        request = self.context.get('request')
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            self.context['ip'] = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            self.context['ip'] = request.META.get("REMOTE_ADDR")
        request = self.context['request']
        icon = 'http://%s%s%s' % (request.META['HTTP_HOST'], settings.MEDIA_URL, user.icon)
        self.context['icon'] = icon
        self.context['token'] = token
        self.context['email'] = user.email
        self.context['id'] = user.id
        self.context['intro'] = user.intro
        return attrs

    # 获取用户
    def _get_user(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        print(password)
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            raise ValidationError({"detail": "邮箱格式不正确"})
        user_obj = UserInfo.objects.filter(email=email).first()
        if user_obj is None:
            raise ValidationError({"detail": "用户名或密码错误"})
        EERROR_PWD = {}
        if not user_obj.check_password(password):

            if email not in EERROR_PWD:
                EERROR_PWD[email] = 1
            else:
                EERROR_PWD[email] += 1
            if EERROR_PWD[email] == 3:
                verification_code = get_code.get_code()
                cache.set(settings.CACHE_LOGIN_SMS % email, verification_code, 120)  # 将验证码存入缓存中，过期时间为2分钟
                print(verification_code)
                res = send_mail(
                    "登录验证码",
                    verification_code,
                    settings.EMAIL_HOST_USER,
                    [email, ], fail_silently=False)
                EERROR_PWD[email] = 0
            raise ValidationError({"detail": "用户名或密码错误"})
        return user_obj

    # def _get_token(self, user):
    #     payload = jwt_payload_handler(user)
    #     token = jwt_encode_handler(payload)
    #     return token


class PutPwdSerilizers(serializers.ModelSerializer):
    code = serializers.CharField(
        required=True,
        min_length=6,
        max_length=6,
        write_only=True,
        error_messages={"blank": "请输入验证码", "required": "请输入验证码", "max_length": "验证码格式错误", "min_length": "验证码格式错误"},
        help_text="验证码")

    re_password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=16,
        error_messages={"blank": "请输入密码", "required": "请输入密码", "max_length": "密码最长16个字符", "min_length": "密码最短8个字符"},
        write_only=True, )
    password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=16,
        error_messages={"blank": "请输入密码", "required": "请输入密码", "max_length": "密码最长16个字符", "min_length": "密码最短8个字符"},
        write_only=True, )

    class Meta:
        model = UserInfo
        fields = ['code', 'email', 'password', 're_password']

    def validate(self, attrs):
        email = str(attrs.get("email"))
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            raise ValidationError({"detail": "邮箱格式不正确"})
        verification_code = str(attrs.get('code'))
        code = cache.get(settings.CACHE_PUTPWD_SMS % email)
        if verification_code != code:
            raise ValidationError({"detail": "验证码错误"})
        attrs.pop('code')
        password = attrs.get('password')
        re_password = attrs.get('re_password')
        if password != re_password:
            raise ValidationError({"detail": "密码不一致"})
        attrs.pop('re_password')
        user = UserInfo.objects.filter(email=email).first()
        user.set_password(password)
        user.save()
        return attrs


class CodeLoginSerilizers(serializers.ModelSerializer):
    code = serializers.CharField(
        required=True,
        min_length=6,
        max_length=6,
        write_only=True,
        error_messages={"blank": "请输入验证码", "required": "请输入验证码", "max_length": "验证码格式错误", "min_length": "验证码格式错误"},
        help_text="验证码")

    class Meta:
        model = UserInfo
        fields = ['id','code', 'email']

    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(user)
        request = self.context.get('request')
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            self.context['ip'] = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            self.context['ip'] = request.META.get("REMOTE_ADDR")
        request = self.context['request']
        icon = 'http://%s%s%s' % (request.META['HTTP_HOST'], settings.MEDIA_URL, user.icon)
        self.context['icon'] = icon
        self.context['email'] = user.email
        self.context['id'] = user.id
        self.context['token'] = token
        return attrs

    def _get_user(self, attrs):
        email = str(attrs.get("email"))
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            raise ValidationError({"detail": "邮箱格式不正确"})
        verification_code = str(attrs.get('code'))
        code = cache.get(settings.CACHE_LOGIN_SMS % email)
        if verification_code != code:
            raise ValidationError({"detail": "验证码错误"})
        attrs.pop('code')
        user = UserInfo.objects.filter(email=attrs['email']).first()
        return user

    def _get_token(self, user):
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

class PasswordPutModelSerializer(serializers.ModelSerializer):
    '''
    修改密码
    '''
    password = serializers.CharField(max_length=18,min_length=6,write_only=True)
    class Meta:
        model = UserInfo
        fields = ['email','password']
        extra_kwargs = {
            'password':{'read_only':False}

        }


    def update(self, instance, validated_data):
        user=UserInfo(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return instance



class UserDetailModelSerializer(serializers.ModelSerializer):
    '''
    用户详情
    '''
    # icon = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    # suffix = serializers.CharField(allow_blank=False)
    class Meta:
        model = UserInfo
        fields = ['id','nickname','intro','icon']

class UserDetailUpdateModelSerializer(serializers.ModelSerializer):
    '''
    修改用户详情
    '''
    icons = serializers.CharField(source='icon',read_only=True)
    class Meta:
        model = UserInfo
        fields = ['nickname','intro','icon','icons']
        extra_kwargs = {
            'icon':{'write_only':True,'required':False}
        }


    def update(self, instance, validated_data):
        instance.icon = self.instance.icon if validated_data.get('icon') is None else validated_data.get('icon')
        instance.nickname = validated_data.get('nickname', self.instance.nickname)
        instance.intro = validated_data.get('intro', self.instance.intro)
        instance.save()
        return instance

from celery_task.user_auth import send_parse
class AuthenticationPostModelSerializer(serializers.ModelSerializer):
    id_number = serializers.SerializerMethodField()
    class Meta:
        model = Authentication_tab
        fields = ['email','name','id_number','the_front_of_id_card','reverse_side_of_id_card','verify_status']
        # fields = '__all__'
    def get_id_number(self,obj):

        idnum = str(obj.id_number)
        idnum = idnum[:4]+'********'+idnum[14:]
        return idnum



    def create(self, validated_data):
        print(validated_data)
        print(validated_data['email'])
        auth=Authentication_tab.objects.create(**validated_data)
        auth.save()
        auth_obj=Authentication_tab.objects.filter(email=auth.email).first()
        print(auth_obj)
        the_front_of_id_card = auth_obj.the_front_of_id_card  # 身份证正面
        print(the_front_of_id_card)
        print(auth_obj)
        auth_obj = Authentication_tab.objects.filter(id=auth_obj.id).first()
        # reverse_side_of_id_card=serializer.data.get('reverse_side_of_id_card') # 身份证反面
        img_path = os.path.join(settings.MEDIA_ROOT, str(auth_obj.the_front_of_id_card))
        print(img_path)
        appcode = "6bb606c906f44a96a2937b2d55d6053c"
        send_parse.delay(appcode,img_path, auth_obj.email)

        # res = parse(appcode, img_path)
        # print(res)
        # dict_data = json.loads(res)
        # print(dict_data)
        # if dict_data.get('success') == True and dict_data.get('is_fake') == False:
        #     auth_obj.address = dict_data.get('address')
        #     auth_obj.birth = dict_data.get('birth')
        #     auth_obj.nationality = dict_data.get('nationality')
        #     auth_obj.sex = dict_data.get('sex')
        #     auth_obj.verify_status = 3
        #     auth_obj.save()
        #     return auth_obj
        # else:
        return auth_obj