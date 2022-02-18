from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Iot
from django.conf import settings
import os

@method_decorator(csrf_exempt, name='dispatch')
class IotAPI(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        if data.get('sn') is None:
            return Response({'detail': 'No SN Code'})
        elif data.get('model') is None:
            return Response({'detail': 'No Model'})
        elif data.get('manufacturer') is None:
            return Response({'detail': 'No Manufacturer'})
        else:
            ip = self.request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get(
                'HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
            try:
                import geoip2.database
                client = geoip2.database.Reader(os.path.join(settings.BASE_DIR, 'utils/GeoLite2-City.mmdb'))
                response = client.city(str(ip))
                Iot.objects.create(sn_code=data.get('sn'),
                                       model_code=data.get('model'),
                                       manufacturer_code=data.get('manufacturer'),
                                       ip=ip,
                                       iso_code=response.country.iso_code,
                                       city=response.city.names.get('en'),
                                       country=response.country.names.get('en'),
                                       continent=response.continent.names.get('en'),
                                       detail=str(response),
                                       meta_detail=str(self.request.META))
            except:
                Iot.objects.create(sn_code=data.get('sn'),
                                       model_code=data.get('model'),
                                       manufacturer_code=data.get('manufacturer'),
                                       ip=ip,
                                       iso_code='NO',
                                       city='NO',
                                       country='NO',
                                       continent='NO',
                                       detail='NO',
                                       meta_detail=str(self.request.META))
            return Response({'detail': 'success'})
