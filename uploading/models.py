from django.db import models

# Create your models here.

from utils.model import BaseModel


import os
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.conf import settings




class Uploading(BaseModel):
    barcode_scanner = models.FileField(upload_to = 'scanner/',blank=True,verbose_name='扫描枪安装包')
    mac = models.FileField(upload_to = 'mac/',blank=True,verbose_name='苹果客户端')
    win = models.FileField(upload_to = 'win64/',blank=True,verbose_name='windows客户端')
    android = models.FileField(upload_to = 'android/',blank=True,verbose_name='安卓客户端')

    class Meta:
        db_table = 'homepage_uploading'
        verbose_name = '软件上传表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s ,%s ,%s ,%s"%(self.barcode_scanner,self.mac,self.win,self.android)



## 添加监听器
@receiver(post_delete, sender=Uploading)
def delete_upload_files(sender, instance, **kwargs):
    files = getattr(instance, 'mac')
    if not files:
        return
    fname = os.path.join(settings.MEDIA_ROOT ,str(files))
    if os.path.isfile(fname):
        os.remove(fname)
    pass

@receiver(post_delete, sender=Uploading)
def delete_upload_files(sender, instance, **kwargs):
    files = getattr(instance, 'win')
    if not files:
        return
    fname = os.path.join(settings.MEDIA_ROOT ,str(files))
    if os.path.isfile(fname):
        os.remove(fname)
    pass

@receiver(post_delete, sender=Uploading)
def delete_upload_files(sender, instance, **kwargs):
    files = getattr(instance, 'scanner')
    if not files:
        return
    fname = os.path.join(settings.MEDIA_ROOT ,str(files))
    if os.path.isfile(fname):
        os.remove(fname)
    pass

@receiver(post_delete, sender=Uploading)
def delete_upload_files(sender, instance, **kwargs):
    files = getattr(instance, 'android')
    if not files:
        return
    fname = os.path.join(settings.MEDIA_ROOT ,str(files))
    if os.path.isfile(fname):
        os.remove(fname)
    pass





