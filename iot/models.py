from django.db import models

class Iot(models.Model):
    sn_code = models.CharField(max_length=255, verbose_name="sn码")
    model_code = models.CharField(max_length=255, verbose_name="model码")
    manufacturer_code = models.CharField(max_length=255, verbose_name="manufacturer码")
    ip = models.CharField(max_length=32, verbose_name="ip地址")
    iso_code = models.CharField(max_length=255, verbose_name="国际编码")
    city = models.CharField(max_length=255, verbose_name="城市")
    country = models.CharField(max_length=255, verbose_name="国家")
    continent = models.CharField(max_length=255, verbose_name="大洲")
    detail = models.TextField(max_length=255, verbose_name="明细")
    auths = models.CharField(default='success', max_length=255, verbose_name="授权")
    meta_detail = models.TextField(max_length=255, verbose_name="meta")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")

    class Meta:
        db_table = 'iot'
        verbose_name = 'data id'
        verbose_name_plural = "data id"
        ordering = ['-create_time']

    def __str__(self):
        return self.pk