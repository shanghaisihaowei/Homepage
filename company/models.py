from django.db import models

# Create your models here.

from utils.model import BaseModel

class MarketUpload(BaseModel):
    imge = models.ImageField(upload_to='market',verbose_name='图片')
    is_show = models.BooleanField(default=True,verbose_name='是否展示')




class Recorder(models.Model):

    hosts = models.CharField(max_length=64,null=True,blank=True,verbose_name='HTTP_HOST')
    referers = models.CharField(max_length=128,null=True,blank=True,verbose_name='HTTP_REFERER')
    mod = models.CharField(max_length=128,null=True,blank=True,verbose_name='访问方式')
    more = models.CharField(max_length=200,null=True,blank=True,verbose_name='META详细')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'homepage_recorder'
        verbose_name = '记录器'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % str(self.hosts)



class HomeBanner(models.Model):
    mode_choices = ((1,'PC官网'),(2,'手机官网'))
    title = models.CharField(max_length=128,blank=True,verbose_name='名称')
    image = models.ImageField(upload_to='banner',null=True,blank=True, verbose_name='图片')
    link = models.CharField(max_length=64,blank=True, verbose_name='跳转链接')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    is_show = models.BooleanField(default=True, verbose_name='是否上架')
    orders = models.IntegerField(verbose_name='优先级')
    mode = models.SmallIntegerField(choices=mode_choices,default=1,verbose_name='模式')
    class Meta:
        db_table = 'homepage_homebanner'
        verbose_name='官网广告位轮播图'
        verbose_name_plural=verbose_name

    def __str__(self):
        return "%s"%str(self.title)


class ArticleBanner(models.Model):
    community_choices  = ((0,'GreaterWMS开源社区'),(1,'DVAdmin社区'))
    language_select = ((0,'中文'),(1,'英文'))
    title = models.CharField(max_length=128, blank=True, verbose_name='名称')
    image = models.ImageField(upload_to='banner', null=True, blank=True, verbose_name='图片')
    link = models.CharField(max_length=64, blank=True, verbose_name='跳转链接')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    is_show = models.BooleanField(default=True, verbose_name='是否上架')
    orders = models.IntegerField(verbose_name='优先级')
    community = models.SmallIntegerField(choices = community_choices,default=0,verbose_name='归属社区')
    language = models.SmallIntegerField(choices=language_select,default=0,verbose_name='语言')

    class Meta:
        db_table = 'homepage_article_banner'
        verbose_name='文章广告位轮播图'
        verbose_name_plural=verbose_name

    def __str__(self):
        return "%s"%str(self.title)

class MobileArticleBanner(models.Model):
    community_choices = ((0, 'GreaterWMS开源社区'), (1, 'DVAdmin社区'))
    language_select = ((0, '中文'), (1, '英文'))
    title = models.CharField(max_length=128, blank=True, verbose_name='名称')
    image = models.ImageField(upload_to='banner', null=True, blank=True, verbose_name='图片')
    link = models.CharField(max_length=64, blank=True, verbose_name='跳转链接')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    is_show = models.BooleanField(default=True, verbose_name='是否上架')
    orders = models.IntegerField(verbose_name='优先级')
    community = models.SmallIntegerField(choices=community_choices, default=0, verbose_name='归属社区')
    language = models.SmallIntegerField(choices=language_select,default=0, verbose_name='语言')


    class Meta:
        db_table = 'homepage_mobile_article_banner'
        verbose_name='手机文章广告位轮播图'
        verbose_name_plural=verbose_name

    def __str__(self):
        return "%s"%str(self.title)