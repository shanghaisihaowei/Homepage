from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from utils.model import BaseModel
import uuid
import os


def user_directory_path(instance, filename):

    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file
    return os.path.join(str(instance.pk), "", filename)

# 一对一用户表

class Authentication_tab(BaseModel):
    """
    实名认证表
    {"address":"海口市琼山区府城镇红星村委会公务村22号","angle":90,"birth":"19961221","card_region":[{"x":70,"y":130},{"x":1012,"y":175},{"x":955,"y":1532},{"x":110,"y":1549}],"config_str":"{\"side\":\"face\"}","face_rect":{"angle":90,"center":{"x":583,"y":1254},"size":{"height":494,"width":396}},"face_rect_vertices":[{"x":833,"y":1449},{"x":338,"y":1455},{"x":333,"y":1059},{"x":828,"y":1053}],"is_fake":false,"name":"陈昌晓","nationality":"汉","num":"460004199612210618","request_id":"0D721181-18B2-492F-8F04-3346EE9C908E","sex":"男","success":true}

    """
    status_type = ((0, "提交信息"), (1, "审核中"), (2, "完成认证"),(3,'认证失败'))
    email = models.CharField(max_length=32,verbose_name='用户邮箱')
    name = models.CharField(max_length=64,verbose_name='真实姓名')
    id_number = models.CharField(max_length=18,verbose_name='身份证号')
    the_front_of_id_card = models.ImageField(upload_to=user_directory_path,verbose_name='身份证正面')
    reverse_side_of_id_card = models.ImageField(upload_to=user_directory_path,verbose_name='身份证反面')
    verify_status = models.SmallIntegerField(choices=status_type,default=0,verbose_name='审核状态')
    address = models.CharField(max_length=64,verbose_name='住址',null=True,blank=True)
    birth = models.CharField(max_length=32,verbose_name='出生年月',null=True,blank=True)
    nationality = models.CharField(max_length=32,verbose_name='民族',null=True,blank=True)
    sex = models.CharField(max_length=16,verbose_name='性别',null=True,blank=True)

    class Meta:
        db_table = 'homepage_authentication_tab'
        verbose_name = '身份认证信息表'
        verbose_name_plural = verbose_name


class UserInfo(AbstractUser, BaseModel):
    gender_type = ((0, "男"), (1, "女"), (2, "其他"))
    type_user = ((0,'普通用户'),(1,'开发者'))
    username = models.CharField(max_length=64, unique=True, null=True)
    mobile = models.CharField(max_length=11, verbose_name='手机号',blank=True)
    icon = models.ImageField(upload_to=user_directory_path, default='icon/default.jpg',null=True, verbose_name='头像')
    # icon = models.TextField()
    is_lock = models.BooleanField(default=False, verbose_name='是否锁定')
    nickname = models.CharField(max_length=128, null=True, blank=True, verbose_name='昵称')
    intro = models.CharField(max_length=100, null=True, blank=True, verbose_name='个性签名')
    gender = models.IntegerField(choices=gender_type, default=0, verbose_name='性别')
    user_type = models.PositiveIntegerField(choices=type_user,default=0,verbose_name='用户类型')
    authentication_tabs = models.OneToOneField(to=Authentication_tab,on_delete=models.SET_NULL,db_constraint=False,null=True,blank=True,verbose_name='认证')
    class Meta:
        db_table = 'homepage_userinfo'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.username)
