from django_filters import FilterSet
from .models import Order

class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
            # "order_id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "total_count": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "currency": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "pay_type": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "status": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "order_id": ['exact', 'iexact', 'contains', 'icontains'],
            "trade_no": ['exact', 'iexact', 'contains', 'icontains'],
            "title": ['exact', 'iexact', 'contains', 'icontains'],
            "affiliation": ['exact', 'iexact'],
            "pay_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "create_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "updata_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "is_delete": ['exact', 'iexact', 'contains', 'icontains'],
        }

