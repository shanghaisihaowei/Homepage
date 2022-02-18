from django.db import models

# Create your models here.
from user.models import UserInfo

from utils.model import BaseModel
import uuid
import os
from ckeditor.fields import RichTextField
from django.db.models import F
def article_directory_path(instance, filename):

    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file
    return os.path.join(str(instance.id), "", filename)


class Article(BaseModel):
    """
    文章表
    """
    community_choices = ((0,'GreaterWMS开源社区'),(1,'DVAdmin社区'),(2,'Quasar Framework'))
    type_choices = ((0, '审核不通过'), (1, '审核已通过'), (2, '未审核'))
    language_choices = ((0, '中文'), (1, '英文'))

    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='文章标题')
    intro = models.CharField(max_length=300, null=True, blank=True, verbose_name='文章简介')
    # cover = models.ImageField(upload_to=article_directory_path, default='cover/default.jpg',null=True,blank=True, verbose_name='文章封面')
    # is_cover = models.BooleanField(default=True,verbose_name='是否有图片')
    content = RichTextField(null=True, blank=True, verbose_name='文章内容')
    author = models.ForeignKey(to=UserInfo, on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False,
                               verbose_name='文章作者')
    check_person = models.SmallIntegerField(choices=type_choices, verbose_name='文章审核状态',default=2)
    language = models.SmallIntegerField(choices=language_choices,default=0,verbose_name='文章语种')
    changed_time = models.DateTimeField(null=True,blank=True,verbose_name='用户修改文章时间')
    community_type = models.SmallIntegerField(choices=community_choices,default=0,verbose_name="社区归属")
    comment_count = models.PositiveIntegerField(verbose_name='评论数', default=0)
    markdown_text = models.TextField(verbose_name='old_text',null=True,blank=True)

    class Meta:
        db_table = 'homepage_article'
        verbose_name = '文章表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '文章标题：%s，文章作者：%s'%(str(self.title),str(self.author.nickname))
