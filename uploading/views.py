from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ViewSet
from . import models
from . import serializers
from utils.APIResponse import APIResponse
from rest_framework.exceptions import APIException
import os
from django.conf import settings

# from .models import delete_upload_files
# class Uploading(ModelViewSet):
#     queryset = models.Uploading.objects.filter().all()
#     serializer_class =serializers.UploadingGetModelSerializer
#
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return APIResponse(result=serializer.data)
#
#
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return APIResponse(result=[])
#     def perform_destroy(self, instance):
#         instance.delete()


class Upload_file(ViewSet):

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        print(file.name.split('.')[-1])
        if file.name == 'Greaterwms.apk':
            new_path = os.path.join(settings.MEDIA_ROOT, 'android', file.name)
            with open(new_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            url_path = request.scheme+'://'+request.META['HTTP_HOST']+settings.MEDIA_URL+'android/'+file.name
            result = {'url_path':url_path}
            return APIResponse(result=result)
        elif file.name =='GreaterWMS.dmg':
            new_path = os.path.join(settings.MEDIA_ROOT, 'mac', file.name)
            with open(new_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            url_path = request.scheme + '://' + request.META['HTTP_HOST'] + settings.MEDIA_URL + 'mac/' + file.name
            result = {'url_path': url_path}
            return APIResponse(result=result)
        elif file.name =='Greaterwms.exe':
            new_path = os.path.join(settings.MEDIA_ROOT, 'windows', file.name)
            # 上传图片
            with open(new_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            url_path = request.scheme + '://' + request.META['HTTP_HOST'] + settings.MEDIA_URL + 'windows/' + file.name
            result = {'url_path': url_path}
            return APIResponse(result=result)
        else:
            raise APIException({'detils':'上传文件名不正确'})
