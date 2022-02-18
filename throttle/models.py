from django.db import models

class ListModel(models.Model):
    ip = models.CharField(max_length=32, verbose_name="IP")
    method = models.CharField(max_length=18, verbose_name="Method")
    t_code = models.CharField(max_length=255, verbose_name="Transaction Code")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")

    class Meta:
        db_table = 'throttle'
        verbose_name = 'data id'
        verbose_name_plural = "data id"
        ordering = ['-id']

    def __str__(self):
        return self.pk
