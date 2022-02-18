import time

from celery_task.celery import app
from utils.send_email import server_exception_message


@app.task()
def send_server_error_message(details):
    """
    :send_company_feedback:异步给公司发送邮件反馈
    :param name:           用户名字
    :param emeil:          用户的邮箱
    :param leave_word:     用户的留言
    :param you_phone:      用户的联系方式
    :param options:        发送状态码
    :return:
    """
    result = server_exception_message(details)
    if result == True:
        return '邮件验证码发送成功'
    else:
        return '邮件验证码发送失败'