
from rest_framework import serializers
from . import models


class HomeBannerGETModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HomeBanner
        fields = ['title','image','link']





class RecorderlistModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Recorder
        fields = ['id','hosts','referers','mod','more','created_time','updated_time','is_delete']





class ArticleBannerGETModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ArticleBanner
        fields = ['title','image','link','community']


class MobileArticleBannerGETModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.MobileArticleBanner
        fields = ['title','image','link','community']