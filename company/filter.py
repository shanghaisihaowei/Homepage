from django_filters import FilterSet
from .models import Recorder,ArticleBanner,MobileArticleBanner
from rest_framework_csv.renderers import CSVStreamingRenderer
class RecorderFilter(FilterSet):
    class Meta:
        model = Recorder
        fields = {
            "id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "hosts": ['exact', 'iexact', 'contains', 'icontains'],
            "referers": ['exact', 'iexact', 'contains', 'icontains'],
            "mod": ['exact', 'iexact', 'contains', 'icontains'],
            "more": ['exact', 'iexact', 'contains', 'icontains'],
            "created_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "updated_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "is_delete": ['exact', 'iexact', 'contains', 'icontains'],
        }



class ArticleBannerFilter(FilterSet):
    class Meta:
        model = ArticleBanner
        fields = {
            "id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "title": ['exact', 'iexact', 'contains', 'icontains'],
            "link": ['exact', 'iexact', 'contains', 'icontains'],
            "created_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "updated_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "is_delete": ['exact', 'iexact', 'contains', 'icontains'],
            "is_show": ['exact', 'iexact', 'contains', 'icontains'],
            "language": ['exact', 'iexact', 'contains', 'icontains'],
            "orders": ['exact', 'iexact', 'contains', 'icontains'],
            "community": ['exact', 'iexact', 'contains', 'icontains'],
        }

class MobileArticleBannerFilter(FilterSet):
    class Meta:
        model = MobileArticleBanner
        fields = {
            "id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "title": ['exact', 'iexact', 'contains', 'icontains'],
            "link": ['exact', 'iexact', 'contains', 'icontains'],
            "created_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "updated_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "is_delete": ['exact', 'iexact', 'contains', 'icontains'],
            "is_show": ['exact', 'iexact', 'contains', 'icontains'],
            "language": ['exact', 'iexact', 'contains', 'icontains'],
            "orders": ['exact', 'iexact', 'contains', 'icontains'],
            "community": ['exact', 'iexact', 'contains', 'icontains'],
        }

def file_headers():
    return [
        'hosts',
        'referers',
        'mod',
        'more',
        'created_time',
        'updated_time',
        'is_delete'
    ]

def cn_data_header():
    return dict([
        ('hosts', u'HTTP_HOST'),
        ('referers', u'HTTP_REFERER'),
        ('mod', u'????????????'),
        ('more', u'META??????'),
        ('created_time', u'?????????'),
        ('updated_time', u'????????????'),
        ('is_delete', u'??????????????????'),
    ])

class FileRenderCN(CSVStreamingRenderer):
    header = file_headers()
    labels = cn_data_header()