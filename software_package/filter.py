from django_filters import FilterSet
from .models import Software

class SoftwareFilter(FilterSet):

    class Meta:
        model = Software
        fields = {
            "id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "name":['exact', 'iexact', 'contains', 'icontains'],
            "brief":['exact', 'iexact', 'contains', 'icontains'],
            "direction_for_use":['exact', 'iexact', 'contains', 'icontains'],
            "rnb":['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "dollar":['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "check":['exact', 'iexact', 'contains', 'icontains'],
            "putaway": ['exact', 'iexact'],
            "people_buy": ['exact', 'iexact', 'contains', 'icontains'],
            "release_form": ['exact', 'iexact', 'contains', 'icontains'],
            "is_delete": ['exact', 'iexact'],
            "affiliation": ['exact', 'iexact'],
            "earnings": ['exact', 'iexact', 'contains', 'icontains', 'gt', 'gte', 'lt', 'lte', 'range'],
            "create_time": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "updata_time": ['year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "soft_label": ['exact', 'iexact'],
        }
