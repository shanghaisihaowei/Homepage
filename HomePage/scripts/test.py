# import random
#
#
# def get_code():
#     code = ''
#     for i in range(4):
#         code += str(random.randint(0, 9))
#     return code
#
# print(get_code())

# from django.core.mail import send_mail
# from django.conf import settings
# email_title = '注册验证码'
# email_body = '6666'
# email = '329025421.com'  # 对方的邮箱
# if __name__ == '__main__':
#
#     send_status = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])

if __name__ == '__main__':


    # import base64
    # import json
    #
    # bytes_str = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IldNUzMyOTAyNTQyMUBxcS5jb20iLCJleHAiOjE2Mzg3ODAyODMsImVtYWlsIjoiMzI5MDI1NDIxQHFxLmNvbSJ9.9IaKVONR9i49JGa5aYSd4uTUwXH8UDorLv35FqsSFWg='
    # res = base64.b64decode(bytes_str)
    #
    # print(res)  # b'{"id": 1, "name": "shawn", "age": "male"}'