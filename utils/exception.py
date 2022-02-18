from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.views import Response
from rest_framework import status
from celery_task.server_mail import send_server_error_message
from utils import HomePage_logging
logger = HomePage_logging.get_logger('HomePage')


def exception_handler(exc, context):
    # 记录日志
    # try:
    #     user_id = context['request'].user.id
    # except:
    #     user_id = '该用户未登录'
    # logger.critical('视图类：%s 出错了，是IP地址为 %s 的用户访问，用户id为： %s ，错误原因是 %s' % (
    #     str(context['view']), context['request'].META.get('REMOTE_ADDR'), user_id, str(exc)))
    # print('视图类：%s 出错了，是IP地址为 %s 的用户访问，用户id为： %s ，错误原因是 %s' % (
    #     str(context['view']), context['request'].META.get('REMOTE_ADDR'), user_id, str(exc)))
    response = drf_exception_handler(exc, context)
    if response is None:
        # 记录服务器异常
        logger.critical('视图%s出错，错误原因：%s' % (str(context['view']),exc))
        send_server_error_message.delay(exc)
        response = Response({'detail': '服务器异常，请重试...'})
    else:
        try:
            msg = response.data['detail']
            if msg == '找不到指定凭据对应的有效用户':
                msg = '用户名或密码错误'
            elif msg == '此令牌对任何类型的令牌无效':
                msg = '服务器升级，登录令牌无效，请退出重新登录！'
            else:
                msg = msg
        except Exception:
            msg = '未知异常'
        response = Response({'code': 998, 'detail': msg})
    return response


