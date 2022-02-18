from django.db import models

# Create your models here.

from ckeditor.fields import RichTextField
from utils.model import BaseModel
from user.models import UserInfo as UserInfos
import time
import os

class Withdrawal_instructions(BaseModel):
    """
    提现说明表
    """
    content = RichTextField(verbose_name='提现说明内容',null=True, blank=True)
    is_show = models.BooleanField(verbose_name='是否展示',default=False)

    class Meta:
        db_table = 'homepage_withdrawal_instructions'
        verbose_name = '提现说明表'
        verbose_name_plural = verbose_name


class Rmb_wallet(BaseModel):
    """
    人民币钱包表
    """
    balance = models.DecimalField(default=0,max_digits=8,decimal_places=2,verbose_name='账户余额（当前总收入）')
    withdrawal_amount = models.DecimalField(default=0,max_digits=8,decimal_places=2,verbose_name='当前可提现金额')
    Platform_extraction_rate = models.DecimalField(default=0.2,max_digits=8,decimal_places=2,verbose_name='平台抽成率')
    userinfos = models.OneToOneField(to=UserInfos, on_delete=models.SET_NULL, db_constraint=False,
                                               null=True, blank=True, verbose_name='用户')
    class Meta:
        db_table = 'homepage_rmb_wallet'
        verbose_name = '人民币钱包表'
        verbose_name_plural = verbose_name

class Rmb_salary_detail(BaseModel):
    """
    人民币收益详情
    """
    email = models.CharField(max_length=32,verbose_name='下单用户邮箱')
    user = models.CharField(max_length=64,verbose_name='下单用户昵称')
    title = models.CharField(max_length=64,verbose_name='详情')
    total = models.DecimalField(max_digits=8,decimal_places=2,default=0,verbose_name='合计金额')
    author = models.ForeignKey(to=UserInfos,on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,verbose_name='关联用户')
    class Meta:
        db_table = 'homepage_rmb_salary_detail'
        verbose_name = '人民币收益详情表'
        verbose_name_plural = verbose_name


class Withdrawal_details(BaseModel):
    """
    人民币提现详情表
    """
    status_type = ((0, "审核失败"), (1, "审核中"), (2, "已打款"),(3, "审核通过"),(4,"待打款"))
    user= models.ForeignKey(to=UserInfos,on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,verbose_name='提现用户')
    balance = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='提现金额')
    withdrawal_type = models.CharField(max_length=32,verbose_name='提现类型')
    Amount_of_money = models.DecimalField(default=0,max_digits=8,decimal_places=2,verbose_name='打款金额')
    verify_status = models.SmallIntegerField(choices=status_type,default=1,verbose_name='审核状态')
    alipay_account = models.CharField(max_length=32,verbose_name='支付宝账户',null=True,blank=True)
    bank_account = models.CharField(max_length=16,verbose_name='银行卡号',blank=True)
    name = models.CharField(max_length=72,verbose_name='开户人',blank=True)
    bankaddr = models.CharField(max_length=64,verbose_name='开户行',blank=True)

    class Meta:
        db_table = 'homepage_withdrawal_details'
        verbose_name = '人民币提现详情表'
        verbose_name_plural = verbose_name

class Dollar_wallet(BaseModel):
    """
    美元钱包表
    """
    balance = models.DecimalField(default=0,max_digits=8,decimal_places=2,verbose_name='账户余额（当前总收入）')
    withdrawal_amount = models.DecimalField(default=0,max_digits=8,decimal_places=2,verbose_name='当前可提现金额')
    Platform_extraction_rate = models.DecimalField(default=0.2,max_digits=8,decimal_places=2,verbose_name='平台抽成率')
    userinfos = models.OneToOneField(to=UserInfos, on_delete=models.SET_NULL, db_constraint=False,
                                     null=True, blank=True, verbose_name='用户')

    class Meta:
        db_table = 'homepage_dollar_wallet'
        verbose_name = '美元钱包表'
        verbose_name_plural = verbose_name

class Dollar_salary_detail(BaseModel):
    """
    美元收益详情
    """
    email = models.CharField(max_length=32,verbose_name='用户邮箱')
    user = models.CharField(max_length=64,verbose_name='下单用户昵称')
    title = models.CharField(max_length=64,verbose_name='详情')
    total = models.DecimalField(max_digits=8,decimal_places=2,default=0,verbose_name='合计金额')
    author = models.ForeignKey(to=UserInfos,on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,verbose_name='关联用户')
    class Meta:
        db_table = 'homepage_dollar_salary_detail'
        verbose_name = '美元收益详情表'
        verbose_name_plural = verbose_name


class Dollar_withdrawal_details(BaseModel):
    """
    美元提现详情表
    """
    status_type = ((0, "审核失败"), (1, "审核中"), (2, "已打款"))
    users= models.ForeignKey(to=UserInfos,on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,verbose_name='提现用户')
    balance = models.DecimalField(default=0,max_digits=8,decimal_places=2,verbose_name='提现金额')
    withdrawal_type = models.CharField(max_length=32,verbose_name='提现类型')
    Amount_of_money = models.DecimalField(default=0,max_digits=8,decimal_places=2,verbose_name='打款金额')
    verify_status = models.SmallIntegerField(choices=status_type,default=1,verbose_name='审核状态')
    paypal_account = models.CharField(max_length=32,verbose_name='paypal账号')

    class Meta:
        db_table = 'homepage_dollar_withdrawal_details'
        verbose_name = '美元提现详情表'
        verbose_name_plural = verbose_name


class Account_bank(BaseModel):
    """
    人民币账户表
    """
    status_type = ((0, "提交信息"), (1, "审核中"), (2, "审核通过"))
    users = models.ForeignKey(to=UserInfos,on_delete=models.DO_NOTHING,null=True,blank=True,db_constraint=False,verbose_name='关联用户')
    name = models.CharField(max_length=32,blank=True,verbose_name='姓名')
    id_number = models.CharField(max_length=18,blank=True,verbose_name='身份证号')
    phone = models.CharField(max_length=11,blank=True,verbose_name='联系电话')
    bank_account = models.CharField(max_length=16,blank=True,verbose_name='银行卡号')
    account_area = models.CharField(max_length=64,blank=True,verbose_name='开户地区')
    bank = models.CharField(max_length=64,blank=True,verbose_name='银行类型')
    bank_location = models.CharField(max_length=64,blank=True,verbose_name='银行位置')
    account_type = models.CharField(max_length=32,blank=True,verbose_name='账号类型',default='银行账户')
    is_default = models.BooleanField(default=False,verbose_name='是否设置为默认账号')
    verify_status = models.SmallIntegerField(choices=status_type,default=0,verbose_name='审核状态')
    class Meta:
        db_table = 'homepage_accout_bank'
        verbose_name = '人民币账户信息表'
        verbose_name_plural = verbose_name

class Usd_account(BaseModel):
    """
    美金账户表
    """
    status_type = ((0, "提交信息"), (1, "审核中"), (2, "审核通过"))
    users = models.ForeignKey(to=UserInfos,on_delete=models.DO_NOTHING,null=True,blank=True,db_constraint=False,verbose_name='关联用户')
    account_number = models.CharField(max_length=32,blank=True,verbose_name='邮箱账号')
    account_type = models.CharField(max_length=32,blank=True,verbose_name='账号类型',default='paypal')
    is_default = models.BooleanField(default=False,blank=True,verbose_name='是否设置为默认账号')
    verify_status = models.SmallIntegerField(choices=status_type,default=0,blank=True,verbose_name='审核状态')
    class Meta:
        db_table = 'homepage_usd_account'
        verbose_name = '美金账户信息表'
        verbose_name_plural = verbose_name


def user_directory_path(instance, filename):

    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(int(round(time.time() * 1000)), ext)
    # return the whole path to the file
    return os.path.join(str(instance.pk), "", filename)




class Rmb_ccount(BaseModel):
    """

    """
    users = models.ForeignKey(to=UserInfos, on_delete=models.DO_NOTHING, null=True, blank=True, db_constraint=False,
                              verbose_name='关联用户')
    alipay_account = models.CharField(max_length=32,blank=True,verbose_name='支付宝账号')
    account_holder = models.CharField(max_length=32,blank=True,verbose_name='开户人')
    account_type = models.CharField(max_length=32,blank=True, verbose_name='账号类型', default='支付宝')
    is_default = models.BooleanField(default=False,blank=True, verbose_name='是否设置为默认账号')

    class Meta:
        db_table = 'homepage_rnb_account'
        verbose_name = '支付宝账户信息表'
        verbose_name_plural = verbose_name
