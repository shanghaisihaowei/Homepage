from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from . import serializers
from . import models
from rest_framework_simplejwt.authentication import JWTAuthentication
import time
from django.utils import timezone
from software_package.models import Software
from rest_framework.exceptions import APIException
from utils.APIResponse import APIResponse
from utils.page import MyPageNumberPagination
import requests
from django.http import HttpResponseRedirect
import qrcode
from bs4 import BeautifulSoup
from utils import HomePage_logging
logger = HomePage_logging.get_logger()
from django.conf import settings
from libs.wechatpay.wepay import get_sign, trans_dict_to_xml, trans_xml_to_dict
from libs.wechatpay import settings as wx_setings
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
import json
from .filer import OrderFilter
from django.db.models import F
from my_wallet.models import Rmb_wallet,Dollar_wallet,Rmb_salary_detail,Dollar_salary_detail,Dollar_salary_detail,Rmb_salary_detail
from django.db import transaction



class OrderAddView(ModelViewSet):
    """
    post:
        create
    """
    authentication_classes = (JWTAuthentication, )
    queryset = models.Order.objects.filter().all()
    serializer_class = serializers.OrderAddModelSerializer

    def create(self, request, *args, **kwargs):
        """
        需要提交的信息：
        1：商品id
        2：商品标题
        3:商品总价
        4：商品总数
        5:币种
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # 1、判断币种
        result_data=self.request.data
        software=result_data.get('software')
        obj=models.Order.objects.filter(user=request.user,software=software,status__in=[2,5,],is_delete=False).first()  # 已支付
        if obj:
            raise APIException({"detail": "您已购买，不能重复购买"})
        status_obj=models.Order.objects.filter(user=request.user, software=software, status__in=[1,], is_delete=False).first()
        if status_obj:
            raise APIException({"detail": "该商品已提交订单，未支付，请去支付"})
        currency=int(result_data.get('currency'))
        if currency == 0 : # 人民币
            software_id = result_data.get('software')
            software_obj = models.Software.objects.filter(id=software_id).first()
            if not software_obj:
                raise APIException({"detail": "提交商品不存在"})
            total_amount = float(result_data.get('total_amount'))
            total_count = int(result_data.get('total_count'))
            if float(total_amount) != float(software_obj.rnb * total_count):
                raise APIException({'detail': "商品价格不合法"})
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:  # 美元
            software_id = result_data.get('software')
            software_obj = models.Software.objects.filter(id=software_id).first()
            if not software_obj:
                raise APIException({"detail": "提交商品不存在"})
            total_amount = float(result_data.get('total_amount'))
            total_count = int(result_data.get('total_count'))
            if total_amount != software_obj.dollar * total_count:
                raise APIException({'detail': "商品价格不合法"})
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # 2、检验价格
        # 3、入库


        # # 验证商品是否存在，
        # result_data=self.request.data
        # software_id=result_data.get('software')
        # software_obj=models.Software.objects.filter(id=software_id).first()
        # if not software_obj:
        #     raise APIException({"detail":"提交商品不存在"})
        # # models.Order.objects.filter(title=result_data.get('title'))
        # # 验证商品价钱是否一致
        # total_amount=float(result_data.get('total_amount'))
        # total_count=int(result_data.get('total_count'))
        # if total_amount != software_obj.rnb*total_count:
        #     raise APIException({'detail':"商品价格不合法"})
        # # 入库
        # # result_data=self.request.data
        # # user=self.request.user
        # # oder_id = timezone.localtime().strftime('%Y%m%d%H%M%S')+('%09d' % user.id)
        # # result_data['oder_id'] = oder_id
        # serializer = self.get_serializer(data=request.data,context={'request':request})
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)

from rest_framework.views import APIView
from libs.ipay.pay import alipay
from libs.ipay.settings import GATEWAY
class AlipayView(APIView):
    authentication_classes = (JWTAuthentication, )
    def get(self,request,*args,**kwargs):
        order_id = self.request.GET.get('order_id')
        order_status = models.Order.objects.filter(status=2, order_id=order_id, user=request.user).first()  # 订单已支付
        if order_status:
            raise APIException({"detail":"您已支付"})
        order_obj = models.Order.objects.filter(status=1, order_id=order_id, user=request.user).first()
        if order_obj is None:
            raise APIException({"detail":"订单信息错误"})
        if order_obj.currency != 0:
            raise APIException({"detail": "订单信息错误"})
        res=alipay.api_alipay_trade_page_pay(
            out_trade_no= order_obj.order_id,
            total_amount=float(order_obj.total_amount),
            subject= order_obj.title,
            return_url= settings.RETURN_URL, #settings.RETURN_URL,  # get回调前端，告诉前端，支付完成情况。
            notify_url= settings.NOTIFY_URL,  # POST异步回调后端，修改商品付款状态
        )
        alipay_url= GATEWAY+res
        result = {"alipay_url": alipay_url}
        return APIResponse(result=result)
class AlipayTransView(APIView):
    def get(self,*args,**kwargs):
        '''
        支付宝转账
        :param args:
        :param kwargs:
        :return:
        '''
        res = alipay.api_alipay_fund_trans_toaccount_transfer(
            123456789, 'ALIPAY_LOGONID', 15203664920, 0.1
        )
        print(res)
        if res['code'] == '10000':
            if res['msg'] == 'Success':
                print('转账成功，交易单号为%s'%res['order_id'])
            return Response('Success')
        else:
            print(res)
        return Response('error')
import datetime
from decimal import Decimal
class PaymentStatusView(APIView):
    # authentication_classes = (JWTAuthentication, )
    def post(self, request):
        # 支付宝post回调，内网测不了
        try:
            result_data = request.POST.dict() # request.data：QueryDict对象（urlencoded），dict对象，QueryDict--》转成dict，对象.dict()
            print(result_data)
            # 订单号，我们给的
            out_trade_no = result_data.get('out_trade_no')
            trade_no = result_data.get('trade_no')  # 支付宝流水号
            print(out_trade_no)
            # 签名
            signature = result_data.pop('sign')
            # sdk的验证签名方法
            result = alipay.verify(result_data, signature)
            if result and result_data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
                # 完成订单修改：订单状态、流水号、支付时间
                pay_time = datetime.datetime.now()
                models.Order.objects.filter(order_id=out_trade_no).update(status=2,pay_type=2,trade_no=trade_no,pay_time=pay_time)  # 修改订单状态为已支付，修改支付方式为支付宝
                order_obj = models.Order.objects.filter(order_id=out_trade_no).first()
                software_obj = models.Software.objects.filter(id=order_obj.software.id).first()
                software_obj.earnings = F('earnings') + order_obj.total_amount  # 软件收益记录
                software_obj.people_buy = F('people_buy') + 1  # 软件购买记录
                # software_obj.number_downloads = F("number_downloads") + 1  # 软件下载记录
                software_obj.save()
                print(order_obj.total_amount)
                # rnb_obj = Rmb_wallet.objects.filter(userinfos=software_obj.user.pk).first()  # 软件作者钱包
                Rmb_wallet.objects.filter(userinfos=software_obj.user.pk).update(balance=F("balance")+order_obj.total_amount, withdrawal_amount=F("withdrawal_amount")+(order_obj.total_amount * Decimal(0.8)))
                # rnb_obj.balance = F('balance') + order_obj.total_amount  # 线包收益更新
                # rnb_obj.withdrawal_amount = rnb_obj.balance - (rnb_obj.balance * 0.2)
                # rnb_obj.withdrawal_amount = F('withdrawal_amount') + (order_obj.total_amount-(order_obj.total_amount * 0.2))
                # rnb_obj.save()
                Rmb_salary_detail.objects.create(author=order_obj.software.user,email=order_obj.user.email,user=order_obj.user.nickname,total=order_obj.total_amount,title=order_obj.title)
                # 完成日志记录
                logger.warning('支付宝：%s订单支付成功' % out_trade_no)
                return Response('success')
            else:
                logger.error('支付宝：%s订单支付失败' % out_trade_no)
        except:
            pass
        return Response('failed')

    def get(self, request):
        # 咱们前端，验证用
        out_trade_no = request.query_params.get('out_trade_no')
        print(out_trade_no)
        try:
            models.Order.objects.get(order_id=out_trade_no, status=2)
            return APIResponse(result=True)
        except:
            return APIResponse(code=101, msg='error', result=False)

class CheckPayView(APIView):
    authentication_classes = (JWTAuthentication, )
    def get(self,request,*args,**kwargs):
        out_trade_no = request.query_params.get('out_trade_no')
        if not out_trade_no:
            raise APIException({"detail":"无效订单号"})
        try:
            order_status = models.Order.objects.filter(status=2, order_id=out_trade_no, user=request.user).first()
            if order_status:
                raise APIException({"detail": "您已支付"})
        except Exception:
            raise APIException({"detail": "订单信息错误"})
        paid = False
        # for i in range(10):
        Time_out = 30  # 30s
        Time = 0
        while True:
            response = alipay.api_alipay_trade_query(out_trade_no)
            print(response)
            code = response.get('code')
            trade_status=response.get('trade_status')
            print(trade_status)
            if response.get('trade_status') == 'TRADE_SUCCESS' and response.get('msg') == 'Success':
                # 完成订单修改：订单状态、流水号、支付时间
                pay_time = datetime.datetime.now()
                print(pay_time)
                trade_no=response.get('trade_no')
                models.Order.objects.filter(order_id=out_trade_no).update(status=2, pay_type=2, trade_no=trade_no,
                                                                          pay_time=pay_time)  # 修改订单状态为已支付，修改支付方式为支付宝
                order_obj = models.Order.objects.filter(order_id=out_trade_no).first()
                software_obj = models.Software.objects.filter(id=order_obj.software.id).first()
                software_obj.earnings = F('earnings') + order_obj.total_amount  # 软件收益记录
                software_obj.people_buy = F('people_buy') + 1  # 软件购买记录
                software_obj.number_downloads = F("number_downloads") + 1  # 软件下载记录
                software_obj.save()
                rnb_obj = Rmb_wallet.objects.filter(userinfos=software_obj.user.pk).first()  # 软件作者钱包
                rnb_obj.balance = F('balance') + order_obj.total_amount  # 线包收益更新
                rnb_obj.withdrawal_amount = rnb_obj.balance - (rnb_obj.balance * 0.2)
                rnb_obj.save()
                Rmb_salary_detail.objects.create(author=order_obj.software.user, email=order_obj.user.email,
                                                 user=order_obj.user.nickname, total=order_obj.total_amount,
                                                 title=order_obj.title)
                # 完成日志记录
                print(out_trade_no)
                logger.warning('支付宝：%s订单支付成功' % out_trade_no)
                return HttpResponseRedirect('/#/market/pluginDetail/' + str(order_obj.out_trade_no))
                # return Response('success')
            # elif code == '40004' or (response.get('trade_status') == "WATI_BUYER_PAY"):

            else:
                # 等待买家付款
                import time
                time.sleep(5)

                Time+=5
                if Time == Time_out:
                    break
                else:
                    continue
        alipay.api_alipay_trade_cancel(out_trade_no=out_trade_no)
        models.Order.objects.filter(order_id=out_trade_no).update(status=6,is_delete=True)  # 修改订单状态为已支付，修改支付方式为支付宝
        return APIResponse(code=101, msg='error,支付失败', result=False)


class Wx(APIView):
    authentication_classes = (JWTAuthentication, )
    def post(self, request):
        data = self.request.data
        try:
            print(request.user.pk)
            print(data['order_id'])
            order_status = models.Order.objects.filter(status=2, order_id=data['order_id'], user=request.user).first()  # 订单已支付
            if order_status:
                raise APIException({"detail": "您已支付"})
            order_obj = models.Order.objects.filter(status=1, order_id=data['order_id'], user=request.user.pk).first()
            print(order_obj)
        except Exception:
            raise APIException({"detail":"订单信息错误"})
        if order_obj:
            if order_obj.currency != 0:
                raise APIException({"detail": "订单信息错误"})
            print(order_obj)
            url = wx_setings.URL  # 微信扫码支付接口
            key = wx_setings.KET  #
            total_fee=int(order_obj.total_amount*int(100))
            print(total_fee)
            # total_fee = order_obj.total_amount*100 # order_obj.total_amount  # 支付金额，单位分
            title = order_obj.title
            body =  title # 商品描述
            out_trade_no = order_obj.order_id
            params = {
                'appid': wx_setings.APPID,  # APPID
                'mch_id': wx_setings.MCH_ID,  # 商户号
                'notify_url': settings.WX_NOTIFY_URL,  # 回调地址
                'product_id': '%s' % out_trade_no,  # 商品编号
                'trade_type': 'NATIVE',  # 支付类型（扫码支付）
                'spbill_create_ip': request.META.get('REMOTE_ADDR'),  # 发送请求服务器的IP地址
                'total_fee': total_fee,  # 订单总金额
                'out_trade_no': out_trade_no,  # 订单编号
                'body': body,  # 商品描述
                'nonce_str': 'ibuaiVcKdpRxkhJA'  # 字符串
            }
            sign = get_sign(params, key)  # 获取签名
            params.setdefault('sign', sign)  # 添加签名到参数字典
            xml = trans_dict_to_xml(params)  # 转换字典为XML
            response = requests.request('post', url, data=xml.encode('utf-8'))  # 以POST方式向微信公众平台服务器发起请求
            data_dict = trans_xml_to_dict(response.content)  # 将请求返回的数据转为字典
            print(data_dict)
            qrcode_name = out_trade_no + '.png'  # 支付二维码图片保存路径
            if data_dict.get('return_code') == 'SUCCESS':  # 如果请求成功
                img_url = data_dict.get('code_url')  # 创建支付二维码片
#                 img = qrcode.make(data_dict.get('code_url'))  # 创建支付二维码片
#                 import os
#                 img_path = os.path.join(settings.MEDIA_ROOT, "%s\\%s" % (self.request.user.pk, out_trade_no + ".png"))
#                 img_url = "%s://%s%s%s/%s" %(request.scheme,request.META['HTTP_HOST'], settings.MEDIA_URL,self.request.user.pk, out_trade_no + ".png")
#                 img.save('%s' % img_path)  # 将二维码保存在用户目录下
                return Response({'img': qrcode_name,'img_url':img_url})
            elif data_dict.get('result_code') == 'FAIL':
                logger.warning('微信预支付：%s订单支付失败' % out_trade_no)
                raise APIException({"detail": "支付失败"})
            else:
                logger.warning('微信预支付：%s订单支付失败' % out_trade_no)
                raise APIException({"detail": "支付失败"})
        else:
            raise APIException({"detail": "支付失败"})

def md5(string):
    import hashlib
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

class NotifyView(APIView):
    """
    支付完成之后的通知
    """
    def post(self,request,*args,**kwargs):
        # 1. 获取结果把结果XML转换为字典格式
        root = trans_xml_to_dict(request.body.decode('utf-8'))
        print(root)
        # 2. 校验签名是否正确，防止恶意请求。
        sign = root.pop('sign')
        # key为商户平台设置的密钥key
        key = wx_setings.KET
        temp = "&".join(
            ["{0}={1}".format(k, root[k]) for k in sorted(root)] + ["{0}={1}".format("key", key, ), ])
        local_sign = md5(temp).upper()
        out_trade_no = root.get('out_trade_no')
        # 签名一致
        if local_sign == sign:
            # 根据订单号，把数据库的订单状态修改为支付成功

            pay_time = datetime.datetime.now()
            models.Order.objects.filter(order_id=out_trade_no).update(status=2,pay_type=1,pay_time=pay_time)
            order_obj=models.Order.objects.filter(order_id=out_trade_no).first()
            software_obj=models.Software.objects.filter(id = order_obj.software.id).first()
            software_obj.earnings = F('earnings') + order_obj.total_amount  # 软件收益记录
            software_obj.people_buy = F('people_buy') + 1
            software_obj.number_downloads = F("number_downloads") + 1
            software_obj.save()
            rnb_obj=Rmb_wallet.objects.filter(userinfos=software_obj.user.pk).first() # 软件作者钱包更新
            rnb_obj.balance = F('balance')+order_obj.total_amount
            rnb_obj.withdrawal_amount = rnb_obj.balance-(rnb_obj.balance * 0.2)
            rnb_obj.save()
            Rmb_salary_detail.objects.create(author=order_obj.software.user,email=order_obj.user.email,user=order_obj.user.nickname,total=order_obj.total_amount,title=order_obj.title)

            logger.warning('微信支付：%s订单支付成功' % out_trade_no)
            response = """<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"""
            return Response(response)
        else:
            print(out_trade_no)
            logger.warning('微信支付：%s订单支付失败' % out_trade_no)
            return Response({'mag':'err'})

class WxBack(APIView):
    """
    统一订单查询接口
    """

    def get(self, request):
        url = wx_setings.ORDER_URL
        # data=request.data
        out_trade_no = str(request.GET.get('out_trade_no'))
        # out_trade_no = data['out_trade_no']  # 支付后的商户订单号
        key = wx_setings.KET  # 商户api密钥
        params = {
            'appid': wx_setings.APPID,  # APPID
            'mch_id': wx_setings.MCH_ID,  # 商户号
            'out_trade_no': out_trade_no,  # 订单编号
            'nonce_str': 'ibuaiVcKdpRxkhJA'  # 随机字符串
        }
        sign = get_sign(params, key)  # 获取签名
        params.setdefault('sign', sign)  # 添加签名到参数字典
        xml = trans_dict_to_xml(params)  # 转换字典为XML
        response = requests.request('post', url, data=xml)  # 以POST方式向微信公众平台服务器发起请求
        data_dict = trans_xml_to_dict(response.content)  # 将请求返回的数据转为字典
        print(data_dict)
        # 支付成功  订单未支付
        if data_dict.get("trade_state_desc") == "支付成功":
            logger.warning('微信：%s订单支付成功' % out_trade_no)
            return Response({"msg": 'ok'})
        else:
            return Response({"msg": 'non-payment'})


import paypalrestsdk

from libs.papay import settings as pa_settings
class PayPal(APIView):
    authentication_classes = (JWTAuthentication, )
    def get(self, request):
        order_id = self.request.GET.get('order_id')
        try:
            order_obj = models.Order.objects.filter(status=1, order_id=order_id, user=request.user).first()
            print(order_obj)
        except Exception:
            raise APIException({"detail": "订单信息错误"})
        if order_obj:
            if order_obj.currency != 1:
                raise APIException({"detail": "订单信息错误"})
            paypalrestsdk.configure({
                "mode": pa_settings.MODE,  # sandbox代表沙盒
                "client_id": pa_settings.CLIENT_ID,
                "client_secret": pa_settings.CLIENT_SECRET
            })

            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": settings.PA_RETURN_URL,  # 支付成功跳转页面
                    "cancel_url": settings.PA_CANCEL_URL    # 取消支付页面
                },
                "transactions": [{
                    "amount": {
                        "total": str(order_obj.total_amount),
                        "currency": "USD"},
                    "description": order_obj.title}]})

            if payment.create():
                payment_id=payment.id
                models.Order.objects.filter(status=1, order_id=order_id, user=request.user).update(payment_id=payment_id,pay_type=3)

                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = str(link.href)
                        print("Redirect for approval: %s" % (approval_url))
                        return Response({"url": approval_url})  # 返回支付链接
            else:
                print(payment.error)
                logger.warning('Paypal预支付：%s订单支付成功' % order_id)
                return Response({"msg": "支付失败"})


class PayBack(APIView):
    def get(self,request):
        # ?paymentId=PAYID-L7UHJGA6ED88532FU3155144&token=EC-6AR335876U336883C&PayerID=73S3E9HVESDX4
        payment_id = request.GET.get("paymentId")  # 订单id
        payerid = request.GET.get("PayerID")  # 支付者id
        print(payerid)
        print(payment_id)
        try:
            payment = paypalrestsdk.Payment.find(payment_id)  # 查询订单明细
        except:
            return Response('err')
        try:
            order_obj = models.Order.objects.get(payment_id=payment_id)
        except:
            return Response('err')
        if payment.execute({"payer_id": payerid}):
            order_obj.status=2
            order_obj.payerid = payerid
            order_obj.pay_time = datetime.datetime.now()
            order_obj.save()
            software_obj = models.Software.objects.filter(id=order_obj.software.id).first()
            Dollar_wallet.objects.filter(userinfos=software_obj.user.id).update(balance=F("balance")+order_obj.total_amount, withdrawal_amount=F("withdrawal_amount")+(order_obj.total_amount*Decimal(0.8)))
            # dollar_obj = Dollar_wallet.objects.filter(userinfos=software_obj.user.id).first()
            # dollar_obj.balance = F('balance') + order_obj.total_amount
            # # dollar_obj.withdrawal_amount = dollar_obj.balance - (dollar_obj.balance * 0.2)
            #
            # dollar_obj.withdrawal_amount = F('withdrawal_amount') + (
            #             order_obj.total_amount - (order_obj.total_amount * 0.2))
            # dollar_obj.save()
            software_obj.earnings = F('earnings')+order_obj.total_amount
            software_obj.people_buy = F('people_buy')+1
            # software_obj.number_downloads = F("number_downloads")+1
            software_obj.save()
            Dollar_salary_detail.objects.create(author=order_obj.software.user,email=order_obj.user.email,user=order_obj.user.nickname,total=order_obj.total_amount,title=order_obj.title)
            logger.warning('%sPaypal订单支付成功' % order_obj.order_id)
            # payment_history = paypalrestsdk.Payment.all({"count": 10})
            # print(payment_history.payments)
            return Response("支付成功")
        else:
            print(payment.error)
            return Response("支付失败")

class PayStatus(APIView):
    authentication_classes = (JWTAuthentication, )
    def get(self, request):
        order_id = self.request.GET.get('order_id')
        try:
            status_obj=models.Order.objects.filter(order_id=order_id,is_delete=False,user=request.user).first()
            if status_obj.status == 2:
                return Response({'mag':'ok'})
        except:
            return Response({'mag':False})



"""

根据商品id和与用户id进行查询

"""
class CheckOrder(ModelViewSet):
    queryset = models.Order.objects.filter().all()
    serializer_class = serializers.CheckOrderlistModelSerializer
    authentication_classes = (JWTAuthentication, )
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = OrderFilter
    lookup_field = 'software'
    def get_serializer_class(self):
        if self.action in ['list',]:
            return serializers.CheckOrderlistModelSerializer
        elif self.action in ['retrieve']:
            return serializers.CheckOrderRetrieveModelSerializer
        else:
            return serializers.CheckOrderRetrieveModelSerializer

    def get_object(self):
        if self.request.user:
            return self.request.user.pk
        else:
            return None


    def get_queryset(self):
        if self.get_object() :
            return models.Order.objects.filter(user=self.get_object(),is_delete=False,status=2)
        else:
            return models.Order.objects.none()


    def retrieve(self, request, *args, **kwargs):
        if self.get_object() is None:
            return APIResponse(result=False)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return APIResponse(result=serializer.data)

from rest_framework.generics import GenericAPIView

class Orderstatus(GenericAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.CheckOrderRetrieveModelSerializer
    authentication_classes = (JWTAuthentication, )
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    def get(self,request,*args,**kwargs):
        software=self.request.GET.get('software')
        obj=models.Order.objects.filter(software=software,user=request.user,is_delete=False,status=2).first()
        if obj is None:
            return APIResponse(status=False)
        # result = self.get_serializer(instance=res)
        return APIResponse(status=True)


class MyOrder(ModelViewSet):
    authentication_classes = (JWTAuthentication, )
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['order_id', "create_time", "update_time", ]
    filter_class = OrderFilter
    lookup_field = 'order_id'
    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.CheckOrderlistModelSerializer
        elif self.action in ['retrieve','destroy']:
            return serializers.CheckOrderRetrieveModelSerializer
        else:
            return serializers.CheckOrderRetrieveModelSerializer
    def get_queryset(self):
        if self.request.user:
            return models.Order.objects.filter(user=self.request.user,is_delete=False,status__in=[1,2,]).order_by('-create_time')
        else:
            return models.Order.objects.none()


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return APIResponse(status=204)

    def perform_destroy(self, instance):
        instance.status = 6
        instance.is_delete=True
        instance.save()



