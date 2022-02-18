import json
import urllib, sys
import ssl
from urllib import parse
from urllib.request import Request
from urllib.error import HTTPError



def user_auth(username,idnum):
    host = 'https://idenauthen.market.alicloudapi.com'
    path = '/idenAuthentication'
    method = 'POST'
    appcode = '6bb606c906f44a96a2937b2d55d6053c'
    querys = ''
    bodys = {}
    url = host + path

    bodys['idNo'] = idnum
    bodys['name'] = username
    try:
        post_data = urllib.parse.urlencode(bodys)
        post_data = post_data.encode(encoding='UTF8')
        headers = {'Authorization': 'APPCODE ' + appcode,
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        request = urllib.request.Request(url=url, data=post_data, headers=headers)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        response = urllib.request.urlopen(request)
        content = str(response.read(), 'utf-8')
        content=json.loads(content)
        return content

    except HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))
        from celery_task.server_mail import send_server_error_message
        send_server_error_message.delay("您好,您的服务器实名认证服务包已用完！")
        return {"respCode":1111,'respMessage':"包已用完"}




