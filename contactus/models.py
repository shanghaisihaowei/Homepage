from django.db import models

# Create your models here.
from utils.model import BaseModel


class Contact(BaseModel):
    """
    联系我们表
    """

    options_choices=((0,'有关网站的建议'),(1,'对产品的建议或问题'),(2,'人才招聘'),(3,'商务合作'),(4,'其他'))

    your_name = models.CharField(max_length=64,null=True,blank=True,verbose_name='您的名字')
    your_email = models.EmailField(null=True,blank=True,verbose_name='您的邮箱')
    leave_word = models.CharField(max_length=300,null=True,blank=True,verbose_name='留言')
    your_phone = models.CharField(max_length=20,null=True,blank=True,verbose_name='您的联系方式')
    options = models.SmallIntegerField(choices=options_choices,null=True,blank=True,verbose_name='选项')

    class Meta:
        db_table='homepage_contact'
        verbose_name='联系我们表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return "名字：%s 邮箱：%s 给我们联系"%(str(self.your_name),str(self.your_email))


class Staffemail(BaseModel):
    position_choices = ((0,"产品经理"),(1,"市场经理"),(2,"人事经理"),(3,"公共"))
    position = models.SmallIntegerField(choices=position_choices,verbose_name='职位')
    email = models.EmailField(verbose_name='邮箱',default='329025421@qq.com')

    class Meta:
        db_table='homepage_staffemail'
        verbose_name='联系我们邮箱'
        verbose_name_plural=verbose_name

    def __str__(self):
        return "名字：%s 邮箱：%s 给我们联系"%(str(self.position),str(self.email))



