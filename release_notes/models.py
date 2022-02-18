from django.db import models

# Create your models here.

from utils.model import BaseModel





class Timer_shaft(BaseModel):
      language_choices = ((0,'中文'),(1,'英文'))

      versions = models.CharField(max_length=32,null=True,blank=True,verbose_name='版本号')
      language = models.IntegerField(choices=language_choices,default=0)
      title = models.CharField(max_length=255,verbose_name='迭代标题')
      iteration_time = models.CharField(max_length=32,verbose_name='迭代时间')
      img = models.ImageField(default='icon/porint.svg',verbose_name='节点插槽')
      node = models.BooleanField(default=False,verbose_name='是否是时间节点')


      class Meta:
            db_table = 'homepage_timer_shaft'
            verbose_name = '发行说明'
            verbose_name_plural = verbose_name

      def __str__(self):
            return str(self.title)


class Details(models.Model):
      language_choices = ((0,'中文'),(1,'英文'))
      language = models.IntegerField(choices=language_choices,default=0)
      timer_shaft = models.ForeignKey(to="Timer_shaft",on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False, verbose_name="详细")
      content = models.CharField(max_length=128,verbose_name='详细内容')

      class Meta:
            db_table = 'homepage_timer_details'
            verbose_name = '发行说明详情'
            verbose_name_plural = verbose_name

      def __str__(self):
            return str(self.content)



