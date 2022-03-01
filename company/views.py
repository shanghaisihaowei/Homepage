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
from . import models
from . import serializers
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filter import RecorderFilter,ArticleBannerFilter,MobileArticleBannerFilter
from .filter import FileRenderCN
from utils.page import MyPageNumberPagination
from django.core.cache import cache
from rest_framework.response import Response
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


class HomeBannerlistview(ModelViewSet):
    queryset = models.HomeBanner.objects.filter(is_delete=False, is_show=True).order_by('orders')[
               :settings.BANNER_COUNT]
    serializer_class = serializers.HomeBannerGETModelSerializer

    def get_queryset(self):
        queryset = models.HomeBanner.objects.filter(is_delete=False, is_show=True).order_by('orders')[
                   :settings.BANNER_COUNT]
        return queryset

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.HomeBannerGETModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    # def list(self, request, *args, **kwargs):
    #     home_banner_list = cache.get('home_banner_list_cache')
    #     if not home_banner_list:
    #         serializer = super().list(self, request, *args, **kwargs)
    #         home_banner_list = serializer.data
    #         cache.set('home_banner_list_cache',home_banner_list)
    #     return Response(home_banner_list)



class ArticleBannerView(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    # filter_class = ArticleBannerFilter
    lookup_field = 'id'
    queryset = models.ArticleBanner.objects.filter(is_delete=False,is_show=True).order_by('orders')[:settings.BANNER_COUNT]
    serializers_class = serializers.ArticleBannerGETModelSerializer

    def get_community_type(self):
        community=self.request.query_params.get('community')
        return community

    def get_queryset(self):
        community=self.get_community_type()
        if community:
            queryset = models.ArticleBanner.objects.filter(community=community,is_delete=False,is_show=True).order_by('orders')[:settings.BANNER_COUNT]
        else:
            queryset = models.ArticleBanner.objects.filter(community=0, is_delete=False, is_show=True).order_by(
                'orders')[:settings.BANNER_COUNT]
        return queryset

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.ArticleBannerGETModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)





    # def list(self, request, *args, **kwargs):
    #     article_banner_list = cache.get('article_banner_list_cache')
    #     if not article_banner_list:
    #         serializer = super().list(self, request, *args, **kwargs)
    #         article_banner_list = serializer.data
    #         cache.set('article_banner_list_cache',article_banner_list)
    #     return Response(article_banner_list)


class MobileArticleBannerView(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    # filter_class = MobileArticleBannerFilter
    lookup_field = 'id'
    queryset = models.MobileArticleBanner.objects.filter(is_delete=False, is_show=True).order_by('orders')[
               :settings.BANNER_COUNT]
    serializers_class = serializers.ArticleBannerGETModelSerializer

    def get_community_type(self):
        community = self.request.query_params.get('community')
        return community

    def get_queryset(self):
        community=self.get_community_type()
        if community:
            queryset = models.MobileArticleBanner.objects.filter(community=community,is_delete=False,is_show=True).order_by('orders')[:settings.BANNER_COUNT]
        else:
            queryset = models.MobileArticleBanner.objects.filter(community=0, is_delete=False,
                                                                 is_show=True).order_by('orders')[
                       :settings.BANNER_COUNT]
        return queryset


    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.ArticleBannerGETModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)


# class GreaterWMSArticleBannerView(ModelViewSet):
#     queryset = models.ArticleBanner.objects.filter(is_delete=False,is_show=True,community=0).order_by('orders')[:settings.BANNER_COUNT]
#
#     serializer_class = serializers.ArticleBannerGETModelSerializer


class RecorderlistView(ModelViewSet):
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = RecorderFilter
    def get_queryset(self):
        return models.Recorder.objects.filter(is_delete=False)

    def get_serializer_class(self):
        if self.action in ['list',]:
            return serializers.RecorderlistModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def list(self, request, *args, **kwargs):
        from datetime import datetime
        dt = datetime.now()
        data = (serializers.RecorderlistModelSerializer(instance).data
            for instance in self.filter_queryset(self.get_queryset())
        )
        renderer = FileRenderCN()
        response = StreamingHttpResponse(
            renderer.render(data),
            content_type="text/csv"
        )
        response['Content-Disposition'] = "attachment; filename='supplier_{}.csv'".format(
            str(dt.strftime('%Y%m%d%H%M%S%f')))
        return response


