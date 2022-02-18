from django_filters import FilterSet
from .models import ListModel

class Filter(FilterSet):
    class Meta:
        model = ListModel
        fields = {
            "id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "ip": ['exact', 'iexact', 'contains', 'icontains'],
            "iso_code": ['exact', 'iexact', 'contains', 'icontains'],
            "city": ['exact', 'iexact', 'contains', 'icontains'],
            "country": ['exact', 'iexact', 'contains', 'icontains'],
            "continent": ['exact', 'iexact', 'contains', 'icontains'],
            "create_time": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "update_time": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range']
        }
