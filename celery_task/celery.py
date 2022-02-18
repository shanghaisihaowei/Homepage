from celery import Celery


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HomePage.settings")


broker = 'redis://127.0.0.1:6379/1'
backend = 'redis://127.0.0.1:6379/2'
# include  是一个列表，放被管理的task 的py文件
app = Celery(__name__, backend=backend, broker=broker, include=[
    'celery_task.user_task',# 新写的task，一定要注册
    'celery_task.user_feedback',
    'celery_task.user_order',
    'celery_task.user_auth',
    'celery_task.server_mail',
])

## 注意：worker的启动命令: celery -A celery_task worker  -l info -P eventlet




app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
app.conf.enable_utc = False

####配置定时任务
from datetime import timedelta
from celery.schedules import crontab
app.conf.beat_schedule = {
    'check_order_outtime': {
        # 本次调度的任务
        'task': 'celery_task.user_order.check_order',
        # 定时任务的调度周期
        'schedule': crontab(),   # 每分钟
      	# 'args': (16, 16),  # 注意：任务就是一个函数，所以如果有参数则需要传递
    },

}