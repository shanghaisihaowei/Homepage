import json
import base64
try :
    from urllib.error import HTTPError
    from urllib.request import Request,urlopen
except ImportError:
    from urllib import Request, urlopen, HTTPError

REQUEST_URL = "http://dm-51.data.aliyun.com/rest/160601/ocr/ocr_idcard.json"  # 请求接口


# 将本地图片转成base64编码的字符串，或者直接返回远程图片
def get_img(img_file):
    if img_file.startswith("http"):
        return img_file
    else:
        with open(img_file, 'rb') as f:  # 以二进制读取本地图片
            data = f.read()
    try:
        encodestr = str(base64.b64encode(data),'utf-8')
    except TypeError:
        encodestr = base64.b64encode(data)

    return encodestr

# 发送请求，获取识别信息
def posturl(headers, body):
    try:
        params=json.dumps(body).encode(encoding='UTF8')
        req = Request(REQUEST_URL, params, headers)
        r = urlopen(req)
        html = r.read()
        return html.decode("utf8")
    except HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))

def parse(appcode, img_file, side='face'):
    config = {'side': side}  # face:表示正面；back表示反面

    # 请求体
    body = {"configure": config}
    img_info = get_img(img_file)
    body.update({'image':img_info})

    # 请求头
    headers = {
        'Authorization': 'APPCODE %s' % appcode,
        'Content-Type': 'application/json; charset=UTF-8'
    }

    html = posturl(headers, body)
    return html

if __name__=="__main__":
    # 配置信息
    appcode = "6bb606c906f44a96a2937b2d55d6053c"
    img_file = r"C:\Users\xiao\PycharmProjects\test17\test17\2f646082e85154aaf7cfc21e5e696e0.jpg"

    parse(appcode, img_file)