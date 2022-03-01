from django_filters import FilterSet
from .models import Article

class ArticleFilter(FilterSet):
    class Meta:
        model = Article
        fields = {
            "id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "title": ['exact', 'iexact', 'contains', 'icontains'],
            "intro": ['exact', 'iexact', 'contains', 'icontains'],
            # "cover": ['exact', 'iexact', 'contains', 'icontains'],
            # "is_cover": ['exact', 'iexact'],
            "content": ['exact', 'iexact', 'contains', 'icontains'],
            "comment_count": ['exact', 'iexact', 'contains', 'icontains'],
            # "author": ['exact', 'iexact', 'contains', 'icontains'],
            "check_person": ['exact', 'iexact', 'contains', 'icontains'],
            "language": ['exact', 'iexact', 'contains', 'icontains'],
            "changed_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "community_type": ['exact', 'iexact', 'contains', 'icontains'],
            "create_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "updata_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "is_delete": ['exact', 'iexact', 'contains', 'icontains'],
        }



class TopArticleFilter(FilterSet):
    class Meta:
        model = Article
        fields = {
            "id": ['exact', 'iexact', 'gt', 'gte', 'lt', 'lte', 'isnull', 'in', 'range'],
            "title": ['exact', 'iexact', 'contains', 'icontains'],
            "intro": ['exact', 'iexact', 'contains', 'icontains'],
            # "cover": ['exact', 'iexact', 'contains', 'icontains'],
            # "is_cover": ['exact', 'iexact'],
            "content": ['exact', 'iexact', 'contains', 'icontains'],
            "comment_count": ['exact', 'iexact', 'contains', 'icontains'],
            # "author": ['exact', 'iexact', 'contains', 'icontains'],
            "check_person": ['exact', 'iexact', 'contains', 'icontains'],
            "language": ['exact', 'iexact', 'contains', 'icontains'],
            "changed_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "community_type": ['exact', 'iexact', 'contains', 'icontains'],
            "create_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "updata_time": ['exact', 'iexact', 'year', 'month', 'day', 'week_day', 'gt', 'gte', 'lt', 'lte', 'range'],
            "is_delete": ['exact', 'iexact', 'contains', 'icontains'],
            "top": ['exact', 'iexact', 'contains', 'icontains'],
        }
