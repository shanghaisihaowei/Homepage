from django.db import models

# Create your models here.

from utils.model import BaseModel
import uuid
import os
def user_directory_path(instance, filename):

    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file
    return os.path.join(str(instance.pk), "", filename)


class Certification(BaseModel):
    status_type = ((0,'提交信息'),(1,'审核状态'),(2,'完成状态'))
    email = models.EmailField(verbose_name='邮箱号')
    name = models.CharField(max_length=64,verbose_name='真实姓名')
    id_number = models.CharField(max_length=64,verbose_name='身份证号')
    id_card_img = models.ImageField(upload_to=user_directory_path,verbose_name='身份证正面')
    id_card_img_reverse_side =models.ImageField(upload_to=user_directory_path,verbose_name='身份证反面')
    audit_status = models.IntegerField(choices=status_type,verbose_name='审核状态')
    class Meta:
        db_table = 'homepage_certification'
        verbose_name = '实名认证表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)
