from django.db import models

# Create your models here.

from utils.model import BaseModel

class MarketUpload(BaseModel):
    imge = models.ImageField(upload_to='market',verbose_name='图片')
    is_show = models.BooleanField(default=True,verbose_name='是否展示')







