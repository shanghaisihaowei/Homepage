from rest_framework import serializers

from .models import Timer_shaft,Details

#
class DetailsModelSerializer(serializers.ModelSerializer):

    class Meta:
            model = Details
            fields = ['content']


class Timer_shaftModelSerializer(serializers.ModelSerializer):
    details_set = DetailsModelSerializer(many=True)
    class Meta:
            model = Timer_shaft
            fields = ['id','img','versions','language','title','iteration_time','node','details_set']





