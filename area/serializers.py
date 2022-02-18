from rest_framework import serializers
from .models import ListModel

class AreaGetSerializer(serializers.ModelSerializer):
    ip = serializers.CharField(read_only=True, required=False)
    city = serializers.CharField(read_only=True, required=False)
    country = serializers.CharField(read_only=True, required=False)
    continent = serializers.CharField(read_only=True, required=False)
    class Meta:
        model = ListModel
        ref_name = 'AreaAreaGetSerializer'
        exclude = ['detail', 'id']
        read_only_fields = ['create_time', 'update_time', ]
