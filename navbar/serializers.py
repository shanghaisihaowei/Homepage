

from rest_framework import serializers

from . import models


class NavbarModelSerializer(serializers.ModelSerializer):
    create_time=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updata_time=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = models.Navbar
        fields = ['id','nav_type','darent','name','methods','url','is_external_link','is_show','order','is_delete','create_time','updata_time']





