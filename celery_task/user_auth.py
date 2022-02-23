

import time

from celery_task.celery import app
from utils.id_card_ocr import parse
from utils.id_auth import user_auth
# 发送短信任务
# @app.task()
# def send_sms(phone, code):
#     time.sleep(3)  # 模拟发送短信延迟
#     print('短信发送成功，手机号是：%s，验证码是：%s' % (phone, code))
#     return '短信发送成功'
from user import models
import json
@app.task()
def send_parse(appcode, img_path,email):
    auth_obj=models.Authentication_tab.objects.filter(is_delete=False,email=email).last()

    result = parse(appcode, img_path)
    try:
        dict_data = json.loads(result)
        if dict_data.get('success') == True and dict_data.get('is_fake') == False:
            auth_obj.address = dict_data.get('address')
            auth_obj.birth = dict_data.get('birth')
            auth_obj.nationality = dict_data.get('nationality')
            auth_obj.id_number = dict_data.get('num')
            auth_obj.sex = dict_data.get('sex')
            auth_obj.verify_status = 1
            auth_obj.save()
            content=user_auth(auth_obj.name,auth_obj.id_number)
            if content.get("").get('respCode') == "0000":
                auth_obj.verify_status = 2
                auth_obj.save()
                return True
            else:
                auth_obj.verify_status = 3
                auth_obj.save()
                return False
    except Exception:
        auth_obj.verify_status = 3
        auth_obj.save()
        return False

    # except Exception:
    #     auth_obj.verify_status = 3
    #     auth_obj.save()
    #     return False
