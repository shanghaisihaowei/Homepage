import json

from django.shortcuts import render

# Create your views here.

from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from .models import Navbar
from .serializers import NavbarModelSerializer
from utils.APIResponse import APIResponse
from .files import FileRenderCN, FileRenderEN
class NavbarView(GenericViewSet,ListAPIView):
    '''
    list:
        获取导航
    '''

    queryset = Navbar.objects.filter().all()
    serializer_class = NavbarModelSerializer
    def get_lang(self,data):
        if self.request.user:
            lang = self.request.META.get('HTTP_LANGUAGE')
        else:
            lang = 'en-us'
        if lang == 'zh-hans':
            data_header = FileRenderCN.render(data)
        elif lang == 'en-us':
            data_header = FileRenderEN.render(data)
        else:
            data_header = FileRenderEN.render(data)
        return data_header

    def get_type(self):
        nav_choices = self.kwargs.get('nav_choices')
        return nav_choices

    def get_queryset(self):
        nav_choices = self.get_type()
        if nav_choices:
            return Navbar.objects.filter(is_delete=False,is_show=True,nav_type=nav_choices).order_by("order")
        else:
            return Navbar.objects.filter(is_delete=False,is_show=True,nav_type=1)

    def list(self, request, *args, **kwargs):
        # nav_choices = self.kwargs.get('nav_choices')
        # queryset = Navbar.objects.filter(is_delete=False,is_show=True)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        res = serializer.data
        dict1 = {}
        res1 = json.dumps(res, ensure_ascii=False)  # 转为json
        res2 = json.loads(res1)  # 转为字典
        l = []
        for j in res2:
            if not j["darent"] is None:
                l.append(j)
            continue
        for i in res2:
            if i["darent"] is None:
                dict1[i['id']] = i
        for i in l:
            if "child" not in dict1[i["darent"]]:
                dict1[i['darent']]["child"] = [i, ]
            else:
                dict1[i['darent']]["child"].append(i)
        j = list(dict1.values())
        return APIResponse(code=200,result=j)

"""
[{
    "id":"",
    "nav_type":"",
    "darent":"",
    "methods":"",
    "name":"",
    "url":"",
    "is_external_link":"",
    "is_show":"",
    "order":"",
    "child":[
            {"nav_type":"",
            "darent":"",
            "methods":"",
            "name":"",
            "url":"",
            "is_external_link":"",
            "is_show":"",
            "order":"",
            },
            {"nav_type":"",
            "darent":"",
            "methods":"",
            "name":"",
            "url":"",
            "is_external_link":"",
            "is_show":"",
            "order":"",
            },
            ]
}]

"""

