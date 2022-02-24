
# 1. 必须要继承MiddlewareMixin
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, HttpResponse

from . import models
class Mydd(MiddlewareMixin):
    def process_request(self, request):
        hosts = request.META.get('HTTP_HOST') # 访问者的ip
        mod=request.META.get('HTTP_USER_AGENT') # 访问方式
        referers=request.META.get('HTTP_REFERER') #
        more = request.META
        models.Recorder.objects.create(hosts=hosts ,referers =referers ,mod=mod,more=more)
    def process_response(self,request,response):
        return response