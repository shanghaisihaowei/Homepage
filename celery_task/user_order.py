from celery_task.celery import app
from order.models import Order
from datetime import datetime
from django.conf import settings
@app.task()
def check_order():
    # 查询出所有已经超时的订单
    # 超时条件： 当前时间 > (订单生成时间 + 超时时间)   =====>>>>  (当前时间 - 超时时间) > 订单生成时间
    now = datetime.now().timestamp()
    timeout_number = now - 60*30
    timeout = datetime.fromtimestamp(timeout_number)
    timeout_order_list = Order.objects.filter(status=1, create_time__lte=timeout)
    for order in timeout_order_list:
        order.status = 6
        order.is_delete=True
        order.save()
