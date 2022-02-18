from django.db import models

class ListModel(models.Model):
    ip = models.CharField(max_length=32, verbose_name="ip地址")
    iso_code = models.CharField(max_length=255, verbose_name="国际编码")
    city = models.CharField(max_length=255, verbose_name="城市")
    country = models.CharField(max_length=255, verbose_name="国家")
    continent = models.CharField(max_length=255, verbose_name="大洲")
    detail = models.TextField(max_length=255, verbose_name="明细")
    link_detail = models.TextField(max_length=255, verbose_name="link")
    meta_detail = models.TextField(max_length=255, verbose_name="meta")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'area'
        verbose_name = 'data id'
        verbose_name_plural = "data id"
        ordering = ['-id']

    def __str__(self):
        return self.pk

class CheckModel(models.Model):
    ip = models.CharField(max_length=32, verbose_name="ip地址")
    t_code = models.CharField(max_length=255, verbose_name="校验码")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")

    class Meta:
        db_table = 'check_token'
        verbose_name = 'data id'
        verbose_name_plural = "data id"
        ordering = ['-id']

    def __str__(self):
        return self.pk
