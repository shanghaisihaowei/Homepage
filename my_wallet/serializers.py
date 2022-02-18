
from rest_framework import serializers
from . import models
import re
from rest_framework.exceptions import ValidationError
from user.models import Authentication_tab

from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.core.cache import cache
class Withdrawal_InstructionsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Withdrawal_instructions

        fields = ['content']




class Rmb_walletViewModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Rmb_wallet
        fields = ['balance','withdrawal_amount','Platform_extraction_rate']



class Dollar_walletViewModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Dollar_wallet
        fields = ['balance','withdrawal_amount','Platform_extraction_rate']


class Rmb_salary_detailModelSerializer(serializers.ModelSerializer):
    """
    作者人民币收益详情
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = models.Rmb_salary_detail
        fields = ['create_time','user','total','title']

class Dollar_salary_detailModelSerializer(serializers.ModelSerializer):
    """
    作者美元收益详情
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = models.Rmb_salary_detail
        fields = ['create_time','user','total','title']



class Account_bankGetModelSerializer(serializers.ModelSerializer):
    """
    人民币提现账户序列化
    """

    class Meta:
        model = models.Account_bank
        fields = ['id','bank_account','account_area','bank','bank_location','account_type','is_default','verify_status']

class RmbCcountModelSerializer(serializers.ModelSerializer):
    """
    获取支付宝账号列表
    """
    class Meta:
        model=models.Rmb_ccount
        fields = ['id','users','alipay_account','account_holder','account_type','is_default']



class RmbCcountAddModelSerializer(serializers.ModelSerializer):
    """
    添加支付宝账号
    """
    # users = serializers.SerializerMethodField()
    code = serializers.CharField(
        required=True,
        min_length=6,
        max_length=6,
        write_only=True,
        error_messages={"blank": "请输入验证码", "required": "请输入验证码", "max_length": "验证码格式错误", "min_length": "验证码格式错误"},
        help_text="验证码")
    class Meta:
        model = models.Rmb_ccount
        fields = ['users','alipay_account','account_holder','account_type','is_default','code']

    # def get_user(self, obj):
    #     name_queryset = Authentication_tab.objects.filter(email=obj.users.email, verify_status=3,
    #                                                       is_delete=False).values('name')
    #     return name_queryset

    def validate(self, attrs):

        verification_code = str(attrs.get('code'))
        code = cache.get(settings.CACHE_ACCOUNT_SMS % self.context['request'].user.email)
        attrs.pop('code')
        if verification_code != code:
            raise ValidationError({"detail": "验证码错误"})
        obj=Authentication_tab.objects.filter(email=self.context['request'].user.email).first()
        if obj is None:
            raise ValidationError(detail='未实名认证')
        attrs['account_holder'] = obj.name
        return attrs


    def create(self, validated_data):
        validated_data['users'] = self.context['request'].user
        obj=models.Rmb_ccount.objects.filter(users=validated_data['users'],is_default=True).first()
        if obj is None:
            validated_data['is_default'] = True
            obj=models.Rmb_ccount.objects.create(**validated_data)
        else:
            obj = models.Rmb_ccount.objects.create(**validated_data)
        return obj

from user.models import Authentication_tab,UserInfo
class RmbCcountUpdateModelSerializer(serializers.ModelSerializer):
    """
    修改支付宝账号默认
    """

    class Meta:
        model=models.Rmb_ccount
        fields = ['id','users','alipay_account','account_holder','account_type','is_default']




    def update(self, instance, validated_data):
        instance.is_default = True
        return instance


class UsdAccountModelSerializer(serializers.ModelSerializer):
    """
    获取paypal账号
    """
    class Meta:
        model = models.Usd_account
        fields = ['id','users','account_number','account_type','is_default','verify_status']


class UsdAccountAddModelSerializer(serializers.ModelSerializer):
    """
    创建paypal账号
    """
    code = serializers.CharField(
        required=True,
        min_length=6,
        max_length=6,
        write_only=True,
        error_messages={"blank": "请输入验证码", "required": "请输入验证码", "max_length": "验证码格式错误", "min_length": "验证码格式错误"},
        help_text="验证码")
    class Meta:
        model = models.Usd_account
        fields = ['id','users','account_number','account_type','is_default','verify_status','code']


    def validate(self, attrs):
        verification_code=attrs.get('code')
        code = cache.get(settings.CACHE_ACCOUNT_SMS % self.context['request'].user.email)
        if verification_code !=code:
            raise ValidationError({"detail": "验证码错误"})
        attrs.pop('code')
        return attrs


    def create(self, validated_data):
        validated_data['users'] = self.context['request'].user
        validated_data['account_type'] = 'paypal'
        obj=models.Usd_account.objects.filter(users=validated_data['users']).first()
        if obj is None:
            validated_data['is_default'] = True
            obj=models.Usd_account.objects.create(**validated_data)
        else:
            obj = models.Usd_account.objects.create(**validated_data)
        return obj


class Withdrawal_detailsGetModelSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    withdrawal_type = serializers.SerializerMethodField()
    class Meta:
        model = models.Withdrawal_details
        fields = ['id','user','balance','withdrawal_type','verify_status','create_time']
    def get_withdrawal_type(self,obj):

        lang=self.context['request'].META.get('HTTP_LANGUAGE')
        print(lang)
        if lang == 'zh-hans':
            return '支付宝'
        else:
            return 'alipay'
from decimal import Decimal
class Withdrawal_detailsAddModelSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    # updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    withdrawal_type = serializers.SerializerMethodField()
    class Meta:
        model = models.Withdrawal_details
        fields = ['id', 'balance', 'alipay_account','create_time','withdrawal_type']
    def get_withdrawal_type(self,obj):

        lang=self.context['request'].META.get('HTTP_LANGUAGE')
        print(lang)
        if lang == 'zh-hans':
            return '支付宝'
        else:
            return 'alipay'


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        # validated_data['withdrawal_type'] = '支付宝'
        validated_data['verify_status'] = 1
        # print(validated_data)
        Rmb_wallet_obj=models.Rmb_wallet.objects.filter(userinfos=self.context['request'].user.pk).first()
        if Rmb_wallet_obj.withdrawal_amount-validated_data['balance'] < 0:
            raise ValidationError(detail="提款金额不足")
        else:
            # Rmb_wallet_obj.balance=Rmb_wallet_obj.balance - validated_data['balance']
            Rmb_wallet_obj.withdrawal_amount = Rmb_wallet_obj.withdrawal_amount-validated_data['balance']
            Rmb_wallet_obj.save()
        Withdrawal_details_obj=models.Withdrawal_details.objects.create(**validated_data)
        return Withdrawal_details_obj



class Dollar_withdrawal_detailsGetModelSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    withdrawal_type = serializers.SerializerMethodField()
    # updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    class Meta:
        model = models.Dollar_withdrawal_details
        fields = ['id', 'balance', 'withdrawal_type', 'create_time','verify_status']

    def get_withdrawal_type(self, obj):

        lang = self.context['request'].META.get('HTTP_LANGUAGE')
        print(lang)
        if lang == 'zh-hans':
            if obj.withdrawal_type =='alipay':
                return '支付宝'
            else:
                return str(obj.withdrawal_type)
        else:
            if obj.withdrawal_type == 'alipay':
                return 'alipay'
            else:
                return str(obj.withdrawal_type)



class Dollar_withdrawal_detailsAddModelSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    # updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    class Meta:
        model = models.Dollar_withdrawal_details
        fields = ['id', 'balance','paypal_account','verify_status','withdrawal_type','create_time']

    def create(self, validated_data):
        validated_data['users'] = self.context['request'].user
        # validated_data['withdrawal_type'] = 'paypal'
        validated_data['verify_status'] = 1

        Dollar_wallet_obj=models.Dollar_wallet.objects.filter(userinfos=self.context['request'].user.pk).first()
        if Dollar_wallet_obj.withdrawal_amount-validated_data['balance'] < 0:
            raise ValidationError(detail="提款金额不足")
        else:
            # Dollar_wallet_obj.balance=Dollar_wallet_obj.balance - validated_data['balance']
            Dollar_wallet_obj.withdrawal_amount = Dollar_wallet_obj.withdrawal_amount - validated_data['balance']
            Dollar_wallet_obj.save()
        Withdrawal_details_obj=models.Dollar_withdrawal_details.objects.create(**validated_data)
        return Withdrawal_details_obj


