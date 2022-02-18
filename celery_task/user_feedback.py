import time

from celery_task.celery import app
from utils.send_email import send_company_feedback_email


@app.task()
def send_company_feedback(name,emeil,leave_word,options):
    """
    :send_company_feedback:异步给公司发送邮件反馈
    :param name:           用户名字
    :param emeil:          用户的邮箱
    :param leave_word:     用户的留言
    :param you_phone:      用户的联系方式
    :param options:        发送状态码
    :return:
    """
    result = send_company_feedback_email(name,emeil,leave_word,options)
    if result == True:
        return '邮件验证码发送成功'
    else:
        return '邮件验证码发送失败'