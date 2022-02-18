from django.db import models

# Create your models here.
from user.models import UserInfo
from utils.model import BaseModel
from software_package.models import Software

class Order(BaseModel):
    pay_choices = ((1,'微信'),(2,'支付宝'),(3,'paypla'))
    status_choices = ((1,'待支付'),(2,'已支付'),(3,'代发货'),(4,'代发货'),(5,'已完成'),(6,'已取消'))
    currency_type = ((0,'人民币'),(1,'美元'))
    affiliation_type = ((0,'GreaterWMS'),(1,'DVadmin'))
    order_id = models.CharField(max_length=64,primary_key=True,verbose_name='订单号')
    trade_no = models.CharField(max_length=64, null=True, verbose_name="流水号")
    user = models.ForeignKey(to=UserInfo,on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,related_name='users',verbose_name='下单用户')
    title = models.CharField(max_length=150,verbose_name='订单标题')
    total_count = models.IntegerField(default=1,verbose_name='商品总数')
    currency = models.SmallIntegerField(choices=currency_type,null=True,blank=True,verbose_name='币种')
    total_amount  = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='实付金额')
    pay_type = models.SmallIntegerField(choices=pay_choices,verbose_name='支付方式',null=True,blank=True)
    pay_time = models.DateTimeField(null=True, verbose_name="支付时间")
    status = models.SmallIntegerField(choices=status_choices,default=1,verbose_name='订单状态')
    software = models.ForeignKey(to=Software, on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False,
                      verbose_name='软件商品')
    payment_id = models.CharField(max_length=120,null=True,blank=True,verbose_name='paypal订单号')
    payerid = models.CharField(max_length=120,null=True,blank=True,verbose_name='支付者paypal的id')
    affiliation = models.SmallIntegerField(choices=affiliation_type,default=0,verbose_name='插件归属')
    # brief = models.CharField(max_length=127,null=True,blank=True, verbose_name='插件简介')
    class Meta:
        db_table = 'homepage_order'
        verbose_name = '订单表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.title)


# class OrderGoods(BaseModel):
#     """
#     订单商品（硬件）
#     """
#
#     order = models.ForeignKey(to=Order, related_name='skus', on_delete=models.CASCADE, verbose_name="硬件订单")
#     sku = models.ForeignKey(to=SKU, on_delete=models.PROTECT, verbose_name="硬件商品")
#     count = models.IntegerField(default=1, verbose_name="数量")
#     price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")


class OrderPackage(BaseModel):
    """
    订单商品（软件）
    """
    order = models.ForeignKey(to=Order,related_name='softwares',on_delete=models.SET_NULL,null=True, blank=True, db_constraint=False,
                               verbose_name='软件订单')

    software = models.ForeignKey(to=Software,on_delete=models.SET_NULL,null=True, blank=True, db_constraint=False,
                               verbose_name='软件商品')
    count = models.IntegerField(default=1, verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")

    class Meta:
        db_table = 'homepage_order_order_package'
        verbose_name = '订单商品表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.software.name)