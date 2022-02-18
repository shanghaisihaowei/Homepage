import time

from celery_task.celery import app
from utils.send_email import send_emails
# 发送短信任务
# @app.task()
# def send_sms(phone, code):
#     time.sleep(3)  # 模拟发送短信延迟
#     print('短信发送成功，手机号是：%s，验证码是：%s' % (phone, code))
#     return '短信发送成功'

@app.task()
def send_code_message(type_code, message, email, sendtype,lang):
    result = send_emails(type_code, message, email, sendtype,lang)
    if result == True:
        return '邮件验证码发送成功'
    else:
        return '邮件验证码发送失败'