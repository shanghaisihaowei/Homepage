from django.shortcuts import render
from rest_framework.exceptions import APIException
# Create your views here.
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from .models import Contact
from .serializers import ContactModelSerializer
from utils.APIResponse import APIResponse
from .files import FileRenderCN, FileRenderEN
import re
# from utils.myThrottle import VisitThrottle

from celery_task.user_feedback import send_company_feedback

class ContactView(GenericViewSet,CreateModelMixin):

    queryset = Contact.objects.filter().all()
    serializer_class = ContactModelSerializer
    # throttle_classes = [VisitThrottle,]
    def get_lang(self, data):
        lang = self.request.META.get('HTTP_LANGUAGE')
        return lang

    def create(self, request, *args, **kwargs):
        data = self.request.data
        if len(data['your_name'])== 0 or len(data['leave_word'])==0:
            raise APIException({"detail": "输入框不能为空"})
        if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$',data['your_email']):
            raise APIException({"detail": "请输入正确的邮箱"})
        serializer = super().create(request, *args, **kwargs)
        send_company_feedback.delay(data['your_name'],data['your_email'],data['leave_word'],int(data['options']))
        return APIResponse(code=200,result=serializer.data)

