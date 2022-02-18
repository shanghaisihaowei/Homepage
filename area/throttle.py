from rest_framework.throttling import BaseThrottle
from throttle.models import ListModel
from utils.md5 import Md5
from django.utils import timezone

data = {}

class VisitThrottle(BaseThrottle):
    def allow_request(self, request, view):
        ip = request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get(
            'HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
        if request.method.lower() == "get":
            return True
        elif request.method.lower() == "post":
            ntime = timezone.now()
            ctime = ntime - timezone.timedelta(seconds=1)
            throttle_ctimelist = ListModel.objects.filter(method="country", create_time__lte=ctime)
            for i in throttle_ctimelist:
                i.delete()
            t_code = Md5.md5(ip)
            throttle_allocationlist = ListModel.objects.filter(method="country").order_by('create_time')
            throttle_count = throttle_allocationlist.count()
            if throttle_count == 0:
                ListModel.objects.create(openid='greaterwms', appid='area', ip=ip, method="country", t_code=t_code)
                return True
            else:
                throttle_last_create_time = throttle_allocationlist.first().create_time
                ListModel.objects.create(openid='greaterwms', appid='area', ip=ip, method="post", t_code=t_code)
                allocation_seconds_balance = (ntime - throttle_last_create_time).seconds
                data["visit_check"] = throttle_last_create_time
                if allocation_seconds_balance >= 1:
                    return True
                else:
                    if throttle_count >= 1:
                        return False
                    else:
                        return True
        else:
            return False

    def wait(self):
        ctime = timezone.now()
        wait_time = (ctime - data["visit_check"]).seconds
        balance_time = 1 - wait_time
        return balance_time
