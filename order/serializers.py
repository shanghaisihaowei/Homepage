from rest_framework import serializers

from . import models
from django.utils import timezone
import random
from utils.snow_flake import get_snowflake_uuid
from django.db import transaction
import time
class OrderAddModelSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(required=False)
    software = serializers.IntegerField(write_only=True)
    brief = serializers.SerializerMethodField()
    class Meta:
        model = models.Order
        fields = ['order_id','trade_no','user','title','brief','total_count','total_amount','pay_type','pay_time','status','software','currency','affiliation']
    def get_brief(self,obj):
        obj=models.Software.objects.filter(id=obj.software.id).first()
        return obj.brief

    def get_order_code(self):
        order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')[
                                                                                     -7:]
        return order_no

    def validate(self, attrs):
        '''[('is_delete', False),
         ('title', '扫码枪'),
         ('total_count', 1),
         ('total_amount', Decimal('0.01')),
         ('oder_id', '20220107103923155084206')]'''
        # user=self.context['request'].user
        # order_id = timezone.localtime().strftime('%Y%m%d%H%M%S')+('%d' % user.id)+str(random.randint(10000000,99999999))
        order_id = get_snowflake_uuid()  # 雪花算法生成全局唯一的19位id
        # order_id = self.get_order_code()
        attrs['order_id'] = order_id
        return attrs

    # 验证商品是否存在
    def create(self, validated_data):
        currency=int(validated_data['currency'])
        if currency==0:
            user=self.context['request'].user
            software=validated_data.pop('software')
            software_obj = models.Software.objects.filter(pk=software).first()
            oder_obj=models.Order.objects.create(
                                        currency=currency,
                                        user=user,
                                        software=software_obj,
                                        order_id=validated_data['order_id'],
                                        title=validated_data['title'],
                                        total_count=validated_data['total_count'],
                                        total_amount=validated_data['total_amount'],
                                        affiliation=software_obj.affiliation)
            models.OrderPackage.objects.create(order=oder_obj,software=software_obj,price=validated_data['total_amount']/validated_data['total_count'],count=validated_data['total_count'])
            return oder_obj
        else:
            user = self.context['request'].user
            software = validated_data.pop('software')
            software_obj = models.Software.objects.filter(pk=software).first()
            oder_obj = models.Order.objects.create(
                currency=currency,
                user=user,
                software=software_obj,
                order_id=validated_data['order_id'],
                title=validated_data['title'],
                total_count=validated_data['total_count'],
                total_amount=validated_data['total_amount'],
                affiliation=software_obj.affiliation)

            models.OrderPackage.objects.create(order=oder_obj, software=software_obj,
                                               price=validated_data['total_amount'] / validated_data['total_count'],
                                               count=validated_data['total_count'])

            return oder_obj


class CheckOrderlistModelSerializer(serializers.ModelSerializer):
    """
    查看订单接口
    """
    pay_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    brief = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = models.Order
        fields = ['pay_time','order_id','title','total_count','currency','total_amount','status','software','brief','affiliation']

    def get_brief(self,obj):
        obj=models.Software.objects.filter(id=obj.software.id).first()
        return obj.brief
class CheckOrderRetrieveModelSerializer(serializers.ModelSerializer):
    pay_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    create_time= serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    brief = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')
    pay_type = serializers.CharField(source='get_pay_type_display')
    class Meta:
        model = models.Order
        fields = ['pay_time','create_time','pay_type','order_id','title','total_count','currency','total_amount','status','software','brief','affiliation']

    def get_brief(self,obj):
        obj=models.Software.objects.filter(id=obj.software.id).first()
        return obj.brief

    # def get_pay_type(self,obj):
    #     res=models.Order.objects.filter(order_id=obj).first()
    #     if res.pay_type == 1:
    #         return '微信'
    #     elif res.pay_type == 2:
    #         return '支付宝'
    #     elif res.pay_type == 3:
    #         return 'paypal'
    #     else:
    #         return ''