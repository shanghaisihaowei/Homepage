from django.db import models

# Create your models here.

from utils.model import BaseModel

import datetime
import os
from user.models import UserInfo
# def file_directory_path(instance, filename):
#     ext = filename.split('.')[-1]
#
#     filename = '{}.{}'.format(int(time.time()), ext)
#     # return the whole path to the file
#     return os.path.join(str(instance.pk), "", filename)
# def upload_path_handler():
#     now_time = datetime.datetime.now().strftime('%Y-%m-%d')
#     return "upload/{time}".format(time=now_time)

class Tab(BaseModel):
    """
    发布插件-标签表
    """
    tab_name = models.CharField(max_length=32, verbose_name='标签名')
    software = models.ForeignKey(to='Software', on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False,
                                 related_name='tab_softwares', verbose_name="插件id")


    class Meta:
        db_table = 'homepage_tab'
        verbose_name = '标签表'
        verbose_name_plural = verbose_name


    def __str__(self):
        return str(self.tab_name)


class Software(BaseModel):
    """
    发布插件-插件表
    """
    check_type = ((0,'未审核'),(1,'审核未通过'),(2,'审核已通过'))
    charges_type = ((0,'免费'),(1,'付费'))
    currency_type = ((0,'人民币'),(1,'美元'))
    affiliation_type = ((0,'GreaterWMS'),(1,'DVadmin'))
    affiliation = models.SmallIntegerField(choices=affiliation_type,default=0,verbose_name='插件归属')
    currency = models.SmallIntegerField(choices=currency_type,null=True,blank=True,verbose_name='币种')
    name = models.CharField(max_length=64, verbose_name='插件名称')
    brief = models.CharField(max_length=127,null=True,blank=True, verbose_name='插件简介')
    source_code_file = models.FileField(upload_to='upload/%Y/%m/%d/', verbose_name='源码文件路径')
    direction_for_use = models.TextField(verbose_name='插件使用说明') # 插件介绍
    rnb = models.FloatField(verbose_name='人民币',null=True,blank=True)
    dollar = models.FloatField(verbose_name='美元',null=True,blank=True)
    user = models.ForeignKey(to=UserInfo,on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False,
                               verbose_name='插件作者')
    check = models.SmallIntegerField(choices=check_type,default=0,verbose_name='审核状态')

    putaway = models.BooleanField(default=False,verbose_name='是否上架')

    people_buy = models.PositiveIntegerField(default=0,verbose_name='购买人数')
    number_downloads = models.PositiveIntegerField(default=0,verbose_name='下载人数')
    release_form = models.SmallIntegerField(choices=charges_type,default=0,verbose_name='发布形式')

    earnings = models.DecimalField(max_digits=8,decimal_places=2,default=0,verbose_name='收益')
    comment_count = models.PositiveIntegerField(verbose_name='评论数', default=0)
    # version_type = models.CharField(max_length=32,verbose_name='发布的版本类型',null=True,blank=True)
    direction_markdown_text = models.TextField(verbose_name='插件使用说明副本',null=True,blank=True)
    class Meta:
        db_table = 'homepage_software'
        verbose_name = '插件表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)


class Versions(BaseModel):
    """
    发布插件-版本
    """
    version_type = models.CharField(max_length=32,verbose_name='发布的版本类型',null=True,blank=True)
    version = models.CharField(max_length=32, verbose_name='插件版本')
    plugin_instructions = models.TextField(verbose_name='插件说明') # 更新说明
    software = models.ForeignKey(to='Software', on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False,
                                 related_name='ver_softwares',
                                 verbose_name="插件id")
    plugin_markdown_text = models.TextField(verbose_name='插件说明副本',null=True,blank=True) # 更新说明


    class Meta:
        db_table = 'homepage_versions'
        verbose_name = '发行版本表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.version)




# class PlugVersionLib(BaseModel):
#     '''插件版本库'''
#     source_code_file = models.CharField(max_length=64,verbose_name='插件路径地址')
#     version = models.CharField(max_length=32, verbose_name='插件版本')
#     software = models.ForeignKey(to='Software', on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False,
#                                  related_name='ver_softwares',
#                                  verbose_name="插件id")


class Comment_soft(BaseModel):
    """
    评论表
    """
    type_choices = ((0, '审核不通过'), (1, '审核已通过'), (3, '未审核'))

    check_person = models.SmallIntegerField(choices=type_choices, verbose_name='评论审核状态',default=3)
    user = models.ForeignKey(to=UserInfo,on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,verbose_name='评论人')
    softwares = models.ForeignKey(to=Software,on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,verbose_name='软件id')
    content = models.CharField(max_length=400,verbose_name='评论内容')
    # 自关联. 根评论子评论. 一对多子评论
    root = models.ForeignKey(to="self",on_delete=models.SET_NULL,null=True,blank=True,related_name='roots',db_constraint=False,verbose_name='根评论')
    reply  =models.ForeignKey(to="self",on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,verbose_name='回复人')
    is_author = models.BooleanField(verbose_name='是否是作者',default=False)

    class Meta:
        db_table='homepage_comment_soft'
        verbose_name='评论表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return "评论文章：%s   审核状态：%s  评论用户：%s  评论内容:%s"%(str(self.softwares),self.get_check_person_display(),self.user,self.content)



class Banner(models.Model):
    title = models.CharField(max_length=128,blank=True,verbose_name='名称')
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    link = models.CharField(max_length=64,blank=True, verbose_name='跳转链接')
    info = models.TextField(blank=True,verbose_name='详情')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    is_show = models.BooleanField(default=True, verbose_name='是否上架')
    orders = models.IntegerField(verbose_name='优先级')

    class Meta:
        db_table = 'homepage_banner'
        verbose_name='软件广告位轮播图'
        verbose_name_plural=verbose_name

    def __str__(self):
        return "%s"%str(self.title)
