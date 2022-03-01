from django.shortcuts import render

# Create your views here.
from utils.APIResponse import APIResponse

from . import models
from rest_framework.viewsets import ModelViewSet
from .serializers import ArticleModelSerializer
from .serializers import BrowseArticleModelSerializer
from .serializers import BrowseArticleDetailModelSerializer
from .serializers import ArticleAddModelSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.throttle import VisitThrottle
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from utils.page import MyPageNumberPagination
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.conf import settings
import os
import uuid
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filter import ArticleFilter
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from .serializers import TopArticleViewModelSerializer
from .serializers import TopArticleViewDetailModelSerializer
class Upload(ViewSet):
    authentication_classes = (JWTAuthentication, )
    @action(methods='POST', detail=False)
    def upload_file(self,request):
        """ ckeditor5图片上传 """
        upload = request.FILES.get('upload')
        file_type = upload.name.split('.')[-1]
        if file_type not in ['bmp','jpg','jpeg','png','gif','webp']:
            raise APIException({"detail": "不支持该图片格式"})
        # 生成uuid
        uid = ''.join(str(uuid.uuid4()).split('-'))
        # 修改图片名称
        names = str(upload.name).split('.')
        names[0] = uid
        # 拼接图片名
        upload.name = '.'.join(names)
        # 构造上传路径
        new_path = os.path.join(settings.MEDIA_ROOT, '%s/'%(self.request.user.id), upload.name).replace('\\', '/')
        print(new_path)
        # 上传图片
        with open(new_path, 'wb+') as destination:
            for chunk in upload.chunks():
                destination.write(chunk)

        # 构造要求的数据格式并返回
        filename = upload.name
        url = 'media/%s/'%(self.request.user.id) + filename
        result = [{'url': url,
                   'uploaded': '1',
                   'fileName': filename}]
        return APIResponse(code=200, result=result)



class ArticleView(ModelViewSet):
    """
        retrieve:
            作者查询一篇文章

        list:
            作者查询所有文章

        create:
            新增一篇文章

        delete:
            删除一篇文章

        partial_update:
            修改一篇文章

        update:
            修改一篇文章
    """

    serializer_class = ArticleModelSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated,)
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['pk', "create_time", "update_time", ]
    filter_class = ArticleFilter

    def get_queryset(self):
        lang = self.get_lang()
        if lang == 'zh-hans':   # language=0  显示中文文章
            return models.Article.objects.filter(author=self.request.user.id,
                                                 is_delete=False).order_by('-updata_time')
        else:                   # language=1  显示英文文章
            return models.Article.objects.filter(author=self.request.user.id,
                                                 is_delete=False).order_by('-updata_time')

    def get_serializer_class(self):
        if self.action in ['retrive', 'list','destroy']:
            return ArticleModelSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ArticleAddModelSerializer
        else:
            return ArticleModelSerializer

    def get_lang(self):
        lang = self.request.META.get('HTTP_LANGUAGE')
        return lang

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # result = serializer.data
        return Response(serializer.data)



    def create(self, request, *args, **kwargs):
        data=request.data
        title=request.data.get('title')
        if title is None:
            raise APIException({"detail":"文章标题社区类型未传"})
        if len(title.encode('gb18030')) > 200:
            raise APIException({"detail":"文章超过200个字符"})
        if data.get('community_type') is None:
            raise APIException({"detail":"community_type社区类型未传"})
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        result = serializer.data
        return APIResponse(code=200, result=result)

    def update(self, request, *args, **kwargs):
        serializer = super().update(request, *args, **kwargs)
        result = serializer.data
        return APIResponse(code=200, result=result)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        self.get_serializer(instance=instance, many=False)
        return APIResponse(msg={'msg': '删除文章成功'})


class BrowseArticleView(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    """
    list:
        未登录可以查看 所有文章
        http://0.0.0.0:8000/article/api/v1/Browse/?community_type=0
    retrieve：
        未登录可以查看 单篇文章
        http://0.0.0.0:8000/article/api/v1/Browse/2/?community_type=0

    """
    queryset = models.Article.objects.all()
    serializer_class = BrowseArticleModelSerializer
    # authentication_classes = (JWTAuthentication, )
    pagination_class = MyPageNumberPagination
    throttle_classes = [VisitThrottle, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    filter_class = ArticleFilter
    def get_lang(self):
        lang = self.request.META.get('HTTP_LANGUAGE')
        return lang

    def get_community_type(self):
        community_type=self.request.query_params.get('community_type')
        return community_type
    def get_serializer_class(self):
        if self.action in ['retrive']:
            return BrowseArticleDetailModelSerializer
        elif self.action in ['list']:
            return BrowseArticleModelSerializer
        else:
            return BrowseArticleDetailModelSerializer
    def get_queryset(self):
        community_type = self.get_community_type()
        if community_type:
            lang = self.get_lang()
            if lang == 'zh-hans':
                return models.Article.objects.filter(community_type=community_type,language=0,check_person=1,is_delete=False).order_by('-updata_time')
            else:
                return models.Article.objects.filter(community_type=community_type,language=1,check_person=1,is_delete=False).order_by('-updata_time')
        else:
            if self.action in ['retrive']:
                return models.Article.objects.filter(check_person=1, is_delete=False).order_by('-updata_time')
            else:
                lang = self.get_lang()
                if lang == 'zh-hans':
                    return models.Article.objects.filter(language=0,check_person=1,is_delete=False).order_by('-updata_time')
                else:
                    return models.Article.objects.filter(language=1,check_person=1,is_delete=False).order_by('-updata_time')


    def retrieve(self, request, *args, **kwargs):
        serializer = super().retrieve(request, *args, **kwargs)
        result = serializer.data
        return APIResponse(code=200, result=result)

    def list(self, request, *args, **kwargs):
        serializer = super().list(request, *args, **kwargs)
        result = serializer.data
        return APIResponse(code=200, result=result)




class GreaterWMSTopArticleView(ModelViewSet):
    queryset = models.Article.objects.all()
    # pagination_class = MyPageNumberPagination
    throttle_classes = [VisitThrottle, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    filter_class = ArticleFilter


    def get_lang(self):
        lang = self.request.META.get('HTTP_LANGUAGE')
        return lang

    def get_serializer_class(self):

        if self.action in ['list',]:
            return TopArticleViewModelSerializer
        elif self.action in ['list']:
            return TopArticleViewDetailModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)


    def get_queryset(self):
        lang = self.get_lang()

        if lang == 'zh-hans':
            return models.Article.objects.filter(community_type=0,language=0,check_person=1,is_delete=False,top=True).order_by('-updata_time')
        else:
            return models.Article.objects.filter(community_type=0,language=1,check_person=1,is_delete=False,top=True).order_by('-updata_time')

    def retrieve(self, request, *args, **kwargs):
        serializer = super().retrieve(request, *args, **kwargs)
        result = serializer.data
        return APIResponse(code=200, result=result)

    def list(self, request, *args, **kwargs):
        serializer = super().list(request, *args, **kwargs)
        result = serializer.data
        return APIResponse(code=200, result=result)


class DVAdminTopArticleView(ModelViewSet):
    queryset = models.Article.objects.all()
    # pagination_class = MyPageNumberPagination
    throttle_classes = [VisitThrottle, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    filter_class = ArticleFilter



    def get_lang(self):
        lang = self.request.META.get('HTTP_LANGUAGE')
        return lang

    def get_serializer_class(self):

        if self.action in ['list', ]:
            return TopArticleViewModelSerializer
        elif self.action in ['list']:
            return TopArticleViewDetailModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def get_queryset(self):
        lang = self.get_lang()

        if lang == 'zh-hans':
            return models.Article.objects.filter(community_type=1, language=0, check_person=1, is_delete=False,
                                                 top=True).order_by('-updata_time')
        else:
            return models.Article.objects.filter(community_type=1, language=1, check_person=1, is_delete=False,
                                                 top=True).order_by('-updata_time')

    def retrieve(self, request, *args, **kwargs):
        serializer = super().retrieve(request, *args, **kwargs)
        result = serializer.data
        return APIResponse(code=200, result=result)

    def list(self, request, *args, **kwargs):
        serializer = super().list(request, *args, **kwargs)
        result = serializer.data
        return APIResponse(code=200, result=result)