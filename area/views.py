from rest_framework import viewsets
from rest_framework.views import APIView
from .models import ListModel, CheckModel
from . import serializers, throttle
from utils.throttle import VisitThrottle
from utils.page import MyPageNumberPagination
from utils.md5 import Md5
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .filter import Filter
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import APIException
import os, requests
from rest_framework_simplejwt.authentication import JWTAuthentication


class APIViewSet(viewsets.ModelViewSet):
    """
        list:
            Response a data list（all）

        create:
            Create a data line（post）
    """
    authentication_classes = []
    permission_classes = []
    throttle_classes = [VisitThrottle]
    queryset = ListModel.objects.all()
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = Filter

    def get_queryset(self):
        auth = self.request.GET.get('auth', '')
        if auth:
            if str(auth).lower() == 'singosgu':
                return self.queryset.filter()
            else:
                raise APIException({"detail": "You Don't Have The Authentication1"})
        else:
            raise APIException({"detail": "You Don't Have The Authentication2"})

    def get_serializer_class(self):
        if self.action in ['list', 'create']:
            return serializers.AreaGetSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        ip = self.request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get(
            'HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
        post_man = self.request.META.get('HTTP_POSTMAN_TOKEN', '')
        if post_man:
            raise APIException({"detail": "Please Don't Use PostMan To Post This API"})
        else:
            t_code = Md5.md5(str(timezone.now()))
            CheckModel.objects.create(ip=ip, t_code=t_code)
            if ListModel.objects.filter(ip=ip).exists():
                pass
            else:
                try:
                    import geoip2.database
                    client = geoip2.database.Reader(os.path.join(settings.BASE_DIR, 'utils/GeoLite2-City.mmdb'))
                    response = client.city(str(ip))
                    ListModel.objects.create(ip=ip, iso_code=response.country.iso_code,
                                             city=response.city.names.get('en'),
                                             country=response.country.names.get('en'),
                                             continent=response.continent.names.get('en'), detail=str(response),
                                             link_detail=str(self.request.data), meta_detail=str(self.request.META))
                    return Response({"check_token": t_code}, status=200)
                except:
                    raise APIException({"detail": "Non-Compliance IP Address"})
            return Response({"check_token": t_code}, status=200)

class Area_Check(APIView):
    authentication_classes = (JWTAuthentication,)
    def get(self, request):
        # ip = '114.82.62.63'
        ip = self.request.META.get('HTTP_X_FORWARDED_FOR') if self.request.META.get(
                'HTTP_X_FORWARDED_FOR') else self.request.META.get('REMOTE_ADDR')
        import geoip2.database
        client = geoip2.database.Reader(os.path.join(settings.BASE_DIR, 'utils/GeoLite2-City.mmdb'))
        area = client.city(str(ip))
        return Response({"area": area.country.names.get('en')}, status=200)