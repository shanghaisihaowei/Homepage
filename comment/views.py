from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ViewSetMixin
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from .serializers import CommentPostModelSerializer
from .serializers import CommentGetModelSerializer
from utils.APIResponse import APIResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from .import models
from django.db.models import F
from rest_framework.exceptions import APIException

class CommentGetView(ViewSetMixin,ListAPIView):
    """
    GET:
        list:获取根评论下的所有子评论
    """

    serializer_class = CommentGetModelSerializer
    queryset = models.Comment_sheet.objects.all()

    def get_queryset(self):
        root_id = self.request.query_params.get('root')
        queryset = models.Comment_sheet.objects.filter(root_id=root_id,is_delete=False)
        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return APIResponse(result=serializer.data)




class CommentView(ViewSetMixin,CreateAPIView):
    """
    POST:
        create:创建评论
    """
    authentication_classes = (JWTAuthentication, )
    serializer_class = CommentPostModelSerializer
    queryset = models.Comment_sheet.objects.all()



    def create(self, request, *args, **kwargs):
        if request.user.pk is None:
            raise APIException({'detail':'用户未登录'})
        serializer = self.get_serializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=models.UserInfo.objects.filter(pk=request.user.pk).first()
        serializer.save(user=user)
        article_id=self.request.data.get('article')
        models.Article.objects.filter(id=article_id).update(comment_count = F('comment_count')+1)  # 每评论一次计数一次
        return APIResponse(result=serializer.data)

