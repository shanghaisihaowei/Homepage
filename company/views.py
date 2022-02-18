from django.shortcuts import render

# Create your views here.

import re
import os
import mimetypes
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from django.conf import settings
class Stream_video_View(ViewSet):
    authentication_classes = ()
    def get_lang(self):
        lang = self.request.META.get('HTTP_LANGUAGE')
        if lang:
            if lang == 'zh-hans':
                return lang
            else:
                return lang
        else:
            return 'en-US'

    def file_iterator(self,file_name, chunk_size=8192, offset=0, length=None):
        with open(file_name, "rb") as f:
            f.seek(offset, os.SEEK_SET)
            remaining = length
            while True:
                bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
                data = f.read(bytes_length)
                if not data:
                    break
                if remaining:
                    remaining -= len(data)
                yield data

    @action(methods='GET', detail=False)
    def stream_video(self,request):
        """将视频文件以流媒体的方式响应"""
        lang=self.get_lang()
        if lang == 'zh-hans':
            path = 'video/GreaterWMSCN.mp4'
        elif lang == 'en-US':
            path = 'video/GreaterWMSEN.mp4'
        else:
            path = 'video/GreaterWMSEN.mp4'
        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
        range_match = range_re.match(range_header)
        # path = request.GET.get('path')
        # path = 'video/GreaterWMSCN.mp4'
        path=os.path.join(settings.MEDIA_ROOT, path).replace('\\', '/')
      #这里根据实际情况改变，我的views.py在core文件夹下但是folder_path却只到core的上一层，media也在core文件夹下
        folder_path = os.getcwd().replace('\\', '/')
        # path=folder_path+'/core/'+path #path就是template ？后面的参数的值
        size = os.path.getsize(path)
        content_type, encoding = mimetypes.guess_type(path)
        content_type = content_type or 'application/octet-stream'
        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte) if first_byte else 0
            last_byte = first_byte + 1024 * 1024 * 10
            if last_byte >= size:
                last_byte = size - 1
            length = last_byte - first_byte + 1
            resp = StreamingHttpResponse(self.file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
            resp['Content-Length'] = str(length)
            resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        else:
            resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
            resp['Content-Length'] = str(size)
        resp['Accept-Ranges'] = 'bytes'
        return resp