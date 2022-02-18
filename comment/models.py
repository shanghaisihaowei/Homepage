from django.db import models

# Create your models here.

from utils.model import BaseModel
from article.models import Article
from user.models import UserInfo
class Comment_sheet(BaseModel):
    """
    评论表
    """
    type_choices = ((0, '审核不通过'), (1, '审核已通过'), (3, '未审核'))

    check_person = models.SmallIntegerField(choices=type_choices, verbose_name='评论审核状态',default=3)
    user = models.ForeignKey(to=UserInfo,on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,verbose_name='评论人')
    article = models.ForeignKey(to=Article,on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,verbose_name='软件id')
    content = models.CharField(max_length=400,verbose_name='评论内容')
    # 自关联. 根评论子评论. 一对多子评论
    root = models.ForeignKey(to="self",on_delete=models.SET_NULL,null=True,blank=True,related_name='roots',db_constraint=False,verbose_name='根评论')
    reply  =models.ForeignKey(to="self",on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,verbose_name='回复人')
    is_author = models.BooleanField(verbose_name='是否是作者',default=False)

    class Meta:
        db_table='homepage_comment_sheet'
        verbose_name='评论表'
        verbose_name_plural=verbose_name
    # type_choices = ((0, '审核不通过'), (1, '审核已通过'), (3, '未审核'))
    # article = models.ForeignKey(to=Article,on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,verbose_name='文章id')
    # content = models.CharField(max_length=400,verbose_name='评论内容')
    # user = models.ForeignKey(to=UserInfo,on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,verbose_name='评论人')
    # reply = models.ForeignKey(to="self",on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False,related_name='replys',verbose_name='回复人')
    # depth = models.PositiveIntegerField(default=1,verbose_name='评论层级')
    # root = models.ForeignKey(to="self",on_delete=models.SET_NULL,null=True,blank=True,related_name='roots',db_constraint=False,verbose_name='根评论')
    # check_person = models.SmallIntegerField(choices=type_choices, verbose_name='评论审核状态',default=3)
    #
    # class Meta:
    #     db_table='homepage_comment_sheet'
    #     verbose_name='评论表'
    #     verbose_name_plural=verbose_name

    # def __str__(self):
    #     return "评论文章：%s   审核状态：%s  评论层级：%s  评论用户：%s  评论内容:%s"%(str(self.article),self.get_check_person_display(),self.depth,self.user,self.content)


