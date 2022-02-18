from django.db import models

# Create your models here.
from utils.model import BaseModel


class Navbar(BaseModel):

    nav_choices = ((1,'首页'),(2,'个人中心'))
    nav_type = models.SmallIntegerField(choices=nav_choices,verbose_name='导航栏类型')
    darent = models.ForeignKey(to='Navbar',on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False, verbose_name="上级菜单")
    methods = models.CharField(max_length=32,verbose_name='请求方式')
    name = models.CharField(max_length=128,verbose_name='导航名称')
    url = models.CharField(max_length=128,verbose_name='路由')
    is_external_link = models.BooleanField(default=False,verbose_name='是否是外链')
    is_show = models.BooleanField(default=True,verbose_name='是否展示')
    order = models.SmallIntegerField(default=0,verbose_name='排序')

    class Meta:
        db_table= 'homepage_navbar'
        verbose_name = '导航表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return str(self.name)