from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from . import serializers
from . import models
from utils.APIResponse import APIResponse
from user.models import Authentication_tab
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from utils.page import MyPageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import APIException
class Withdrawal_InstructionsView(ModelViewSet):
    queryset =models.Withdrawal_instructions.objects.filter().all()

    def get_queryset(self):
        return models.Withdrawal_instructions.objects.filter(is_show=True).all()


    def get_serializer_class(self):
        if self.action in ['list',]:
            return serializers.Withdrawal_InstructionsModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return APIResponse(result=serializer.data)

from django.db.models import Avg,Max,Min,Count,Sum
from decimal import Decimal
class Rmb_walletView(ModelViewSet):
    authentication_classes = (JWTAuthentication, )
    # pagination_class = MyPageNumberPagination
    # filter_backends = [DjangoFilterBackend, OrderingFilter, ]


    def get_queryset(self):
        if self.request.user:
            print(self.request.user.pk)
            return models.Rmb_wallet.objects.filter(userinfos=self.request.user.pk)
        else:
            return models.Rmb_wallet.objects.none()

    def get_serializer_class(self):
        if self.action in ['list',]:
            return serializers.Rmb_walletViewModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            Withdrawal_queryset = models.Withdrawal_details.objects.filter(user_id=self.request.user.pk,is_delete=False).all()
            Cumulative=Decimal(0)
            for i in Withdrawal_queryset:
                Cumulative=Cumulative+i.balance

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)

            return APIResponse(result={'data':serializer.data,'Cumulative':Cumulative})
        except Exception:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)

            return APIResponse(result={'data': serializer.data, 'Cumulative': str(0.00)})

class Rmb_salary_detailView(ModelViewSet):
    authentication_classes = (JWTAuthentication, )
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]

    def get_queryset(self):
        if self.request.user:
            return models.Rmb_salary_detail.objects.filter(author=self.request.user.pk)
        else:
            return models.Rmb_salary_detail.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.Rmb_salary_detailModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def list(self, request, *args, **kwargs):
        '''
        查看作者人民币收益详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class Dollar_walletView(ModelViewSet):
    queryset = models.Dollar_wallet.objects.filter().all()
    authentication_classes = (JWTAuthentication, )
    # pagination_class = MyPageNumberPagination
    # filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    def get_queryset(self):
        if self.request.user:
            return models.Dollar_wallet.objects.filter(userinfos=self.request.user.pk)
        else:
            return models.Dollar_wallet.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.Dollar_walletViewModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)
    def list(self, request, *args, **kwargs):
        """
        作者美元钱包
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.filter_queryset(self.get_queryset())
        try:
            Withdrawal_queryset = models.Dollar_withdrawal_details.objects.filter(users_id=self.request.user.pk,
                                                                           is_delete=False).all()
            Cumulative = Decimal(0)
            for i in Withdrawal_queryset:
                Cumulative = Cumulative + i.balance
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return APIResponse(result={'data': serializer.data, 'Cumulative': Decimal(Cumulative)})
        except Exception:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return APIResponse(result={'data': serializer.data, 'Cumulative': str(0.00)})


class Dollar_salary_detailView(ModelViewSet):
    authentication_classes = (JWTAuthentication, )
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]



    def get_queryset(self):
        if self.request.user:
            return models.Dollar_salary_detail.objects.filter(author=self.request.user.pk)
        else:
            return models.Dollar_salary_detail.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.Dollar_salary_detailModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def list(self, request, *args, **kwargs):
        '''
        查看作者美元收益详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class Account_bankView(ModelViewSet):
    """
    list:
            Response a data list（all）
    """

    authentication_classes = (JWTAuthentication, )
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]

    def get_queryset(self):
        if self.request.user:
            return models.Account_bank.objects.filter(users=self.request.user.pk,is_delete=False)
        else:
            return models.Account_bank.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.Account_bankGetModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def list(self, request, *args, **kwargs):
        """
        用户查看人民币账户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class RmbCcountView(ModelViewSet):
    authentication_classes = (JWTAuthentication, )
    lookup_field = 'id'
    def get_queryset(self):
        if self.request.user:
            return models.Rmb_ccount.objects.filter(users=self.request.user.pk,is_delete=False)
        else:
            return models.Rmb_ccount.objects.none()

    def get_serializer_class(self):
        if self.action in ['list','destroy','update']:
            return serializers.RmbCcountModelSerializer
        elif self.action in ['create']:
            return serializers.RmbCcountAddModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        # code=request.data.pop('code')
        #
        email=request.user.email
        # codes = cache.get(settings.CACHE_LOGIN_SMS % email)
        # if codes != code:
        #     raise APIException({'detail':'验证码不正确'})
        obj=Authentication_tab.objects.filter(email=email).first()
        print(request.data)
        if obj is None:
            return APIResponse(result={'msg':'用户未实名认证，请去实名认证'})
        else:
            if obj.verify_status !=2:
                return APIResponse(result={'msg':'用户实名认证未通过，请去实名认证'})
            data = {
                "account_holder":obj.name,
                "alipay_account":request.data.get('alipay_account'),
                "account_type":"支付宝",
                "validated_data":request.user.pk,
                "code":request.data.get('code')
            }
            serializer = self.get_serializer(data=data,context = {'request':request})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            serializer=self.get_serializer(self.get_queryset(),many=True)
            return APIResponse(result={'data':serializer.data})

    def update(self, request, *args, **kwargs):
        try:
            obj=models.Rmb_ccount.objects.filter(users=request.user.pk,is_delete=False).exclude(is_default=False).first()
            obj.is_default=False
            obj.save()
            instance = self.get_object()
            instance.is_default = True
            instance.save()
            serializers=self.get_serializer(instance=self.get_queryset(), many=True)
            return APIResponse(result={'msg': '修改默认账户成功','data':serializers.data})
        except Exception:
            instance = self.get_object()
            instance.is_default = True
            instance.save()
            serializers=self.get_serializer(instance=self.get_queryset(), many=True)
            return APIResponse(result={'msg': '修改默认账户成功','data':serializers.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        obj = models.Rmb_ccount.objects.filter(users=request.user.pk, is_delete=False, is_default=True).first()
        if obj is None:
            default_obj = models.Rmb_ccount.objects.filter(users=request.user.pk, is_delete=False).first()
            if default_obj:
                default_obj.is_default=True
                default_obj.save()
            else:
                self.get_serializer(instance=instance, many=False)
                return APIResponse(result={'msg': '删除账户成功'})
        self.get_serializer(instance=instance, many=False)
        serializers = self.get_serializer(instance=self.get_queryset(), many=True)
        return APIResponse(result={'msg': '删除账户成功','data':serializers.data})






class Usd_accountView(ModelViewSet):
    authentication_classes = (JWTAuthentication, )
    lookup_field = 'id'
    def get_queryset(self):
        if self.request.user:
            return models.Usd_account.objects.filter(users=self.request.user.pk,is_delete=False)
        else:
            return models.Usd_account.objects.none()


    def get_serializer_class(self):
        if self.action in ['list','update','destroy']:
            return serializers.UsdAccountModelSerializer
        elif self.action in ['create']:
            return serializers.UsdAccountAddModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,context = {'request':request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return APIResponse(result={'data':serializer.data})

    def update(self, request, *args, **kwargs):
        try:
            obj=models.Usd_account.objects.filter(users=request.user.pk,is_delete=False).exclude(is_default=False).first()
            obj.is_default=False
            obj.save()
            instance = self.get_object()
            instance.is_default = True
            instance.save()
            serializers=self.get_serializer(instance=self.get_queryset(), many=True)

            return APIResponse(result={'msg': '修改默认账户成功','data':serializers.data})
        except Exception:
            instance = self.get_object()
            instance.is_default = True
            instance.save()
            serializers=self.get_serializer(instance=self.get_queryset(), many=True)
            return APIResponse(result={'msg': '修改默认账户成功','data':serializers.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()

        obj = models.Usd_account.objects.filter(users=request.user.pk,is_delete=False,is_default=True).first()
        if obj is None:
            default_obj=models.Usd_account.objects.filter(users=request.user.pk,is_delete=False).first()
            if default_obj:
                default_obj.is_default=True
                default_obj.save()
            else:
                self.get_serializer(instance=instance, many=False)
                return APIResponse(result={'msg': '删除账户成功'})
        self.get_serializer(instance=instance, many=False)
        serializers = self.get_serializer(instance=self.get_queryset(), many=True)
        return APIResponse(result={'msg': '删除账户成功','data':serializers.data})

from decimal import Decimal
class Withdrawal_detailsView(ModelViewSet):
    authentication_classes = (JWTAuthentication, )
    lookup_field = 'id'

    def get_queryset(self):
        if self.request.user:
            return models.Withdrawal_details.objects.filter(user=self.request.user.pk, is_delete=False)
        else:
            return models.Withdrawal_details.objects.none()

    def get_serializer_class(self):
        if self.action in ['list',]:
            return serializers.Withdrawal_detailsGetModelSerializer
        elif self.action in ['create']:
            return serializers.Withdrawal_detailsAddModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        Rmb_wallet_obj=models.Rmb_wallet.objects.filter(userinfos=request.user.pk).first()
        data=request.data
        print(data)
        if Rmb_wallet_obj is None:
            raise APIException({"detail":"钱包余额不足"})
        else:
            balances=Rmb_wallet_obj.withdrawal_amount  # 可提现金额
            if int(balances) < 800:
                raise APIException({"detail":"提现账户金额必须大于800才可体现"})
            balance=request.data.get('balance')
            if Decimal(balance) < Decimal(800):
                raise APIException({"detail":"提现金额必须大于800才可体现"})
            serializer = self.get_serializer(data=request.data,context={'request':request})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)



class Dollar_withdrawal_detailsView(ModelViewSet):
    authentication_classes = (JWTAuthentication, )
    lookup_field = 'id'

    def get_queryset(self):
        if self.request.user:
            return models.Dollar_withdrawal_details.objects.filter(users=self.request.user.pk, is_delete=False)
        else:
            return models.Dollar_withdrawal_details.objects.none()

    def get_serializer_class(self):
        if self.action in ['list',]:
            return serializers.Dollar_withdrawal_detailsGetModelSerializer
        elif self.action in ['create']:
            return serializers.Dollar_withdrawal_detailsAddModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True,context={'request':request})
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        Dollar_wallet_obj=models.Dollar_wallet.objects.filter(userinfos=request.user.pk).first()
        if Dollar_wallet_obj is None:
            raise APIException({"detail":"钱包余额不足"})
        else:
            balances=Dollar_wallet_obj.balance
            if int(balances) < 100:
                raise APIException({"detail":"提现账户金额必须大于100才可体现"})
            balance=request.data.get('balance')
            if Decimal(balance) < Decimal(100):
                raise APIException({"detail":"提现金额必须大于800才可体现"})
            serializer = self.get_serializer(data=request.data,context={'request':request})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)

from rest_framework.views import APIView
class Withdrawal_current_monthView(APIView):
    authentication_classes = (JWTAuthentication, )
    def get(self,*args,**kwargs):
        models.Withdrawal_details.objects.filter(user=self.request.user.pk, is_delete=False)






