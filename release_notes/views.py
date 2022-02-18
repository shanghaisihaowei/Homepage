from django.shortcuts import render

# Create your views here.
from utils.APIResponse import APIResponse
from rest_framework.viewsets import ModelViewSet
from . import models
from .serializers import Timer_shaftModelSerializer
from .serializers import DetailsModelSerializer





class Timer_shaftView(ModelViewSet):

    queryset = models.Timer_shaft.objects.all()
    serializer_class = Timer_shaftModelSerializer

    def get_lang(self):
        lang = self.request.META.get('HTTP_LANGUAGE')
        return lang

    def get_queryset(self):
        lang = self.get_lang()
        if lang:
            if lang == 'zh-hans':
                return models.Timer_shaft.objects.filter(language=0).order_by('-id')
            else:
                return models.Timer_shaft.objects.filter(language=1).order_by('-id')
        else:
            return models.Timer_shaft.objects.filter(language=1)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        result=serializer.data
        return APIResponse(result=result)






#
class DetailsView(ModelViewSet):

    queryset = models.Details.objects.all()
    serializer_class = DetailsModelSerializer

    def get_lang(self):
        lang = self.request.META.get('HTTP_LANGUAGE')
        return lang

    def get_queryset(self):
        lang = self.get_lang()
        if lang:
            if lang == 'zh-hans':

                return models.Details.objects.filter(language=0)
            else:
                return models.Details.objects.filter(language=1)
        else:
            return models.Details.objects.filter(language=1)
#
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        result=serializer.data
        return APIResponse(result=result)




