
from rest_framework import serializers
from . import models
import re
from rest_framework.exceptions import ValidationError
from django.forms import model_to_dict

from django.conf import settings



class SoftwareReleaseGETModelSerializer(serializers.ModelSerializer):
    '''
    1、用户头像
    2、插件标题
    3、插件简介
    4、插件标签
    5、发布时间
    6、付费类型
    7、价钱
    8、下载次数/购买次数
    '''
    user = serializers.SerializerMethodField()
    tab = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    check = serializers.CharField(source='get_check_display',read_only=True)
    class Meta:
        model = models.Software
        fields =['id','name','brief','user','tab','release_form','rnb','dollar','create_time','updata_time','people_buy','currency','number_downloads','affiliation','earnings','check']

    def get_tab(self,obj):
        queryset=models.Tab.objects.filter(software=obj).values('tab_name')
        return queryset

    def get_user(self, obj):
        request = self.context.get('request')
        icon_url = "%s://%s%s%s" % (request.scheme, request.META['HTTP_HOST'], settings.MEDIA_URL, obj.user.icon)
        return {"id": obj.user.id, "author": obj.user.nickname, "icon": icon_url,'title_tag':obj.user.user_type}


class SoftwareReleaseDetailModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    tab = serializers.SerializerMethodField()
    versions = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M',read_only=True)
    updata_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M',read_only=True)
    comment = serializers.SerializerMethodField()
    class Meta:
        model=models.Software
        fields = ['id','name','brief','user','tab','release_form','direction_for_use','rnb','dollar','create_time','updata_time','versions','people_buy','comment','number_downloads','affiliation','direction_markdown_text']

    def get_tab(self,obj):
        tab_queyset = models.Tab.objects.filter(software = obj).values('tab_name')
        return tab_queyset

    def get_user(self, obj):
        request = self.context.get('request')
        icon_url = "%s://%s%s%s" % (request.scheme, request.META['HTTP_HOST'], settings.MEDIA_URL, obj.user.icon)
        return {"id":obj.user.id,"author": obj.user.nickname, "icon": icon_url,'title_tag':obj.user.user_type}

    def get_versions(self,obj):
        versions_list = []
        versions_queyset = models.Versions.objects.filter(software=obj).values('version','plugin_instructions','updata_time','version_type','plugin_markdown_text')
        for item in versions_queyset:
            item['updata_time'] = item['updata_time'].strftime('%Y-%m-%d')
            versions_list.append(item)
        return versions_list


    def get_comment(self,obj):
        first_queryset=models.Comment_soft.objects.filter(softwares = obj,is_delete = False,root=None).order_by('-id').values(
            'id',
            'content',
            'user__id',
            'user__icon',
            'user__nickname',
            'create_time',
            'softwares',
            'root',
            'is_author',
        )
        queryset_id = models.Comment_soft.objects.filter(softwares=obj, is_delete=False, root=None).order_by(
            '-id').values(
            'id',
        )
        id_list = []
        for item in queryset_id:
            id_list.append(item['id'])
        to_list=models.Comment_soft.objects.filter(softwares=obj, is_delete=False, root__in=id_list).order_by(
            '-id').values(
            'id',
            'content',
            'user__id',
            'user__icon',
            'user__nickname',
            'create_time',
            'softwares',
            'root',
            'reply',
            'reply__user__nickname',
            'is_author',
        )

        request = self.context.get('request')
        for item in first_queryset:
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
            item['user__icon'] = "%s://%s%s%s"%(request.scheme,request.META['HTTP_HOST'],settings.MEDIA_URL,item['user__icon'])
            item['child'] = []
        first_queryset_dict = {}

        for item in first_queryset:
            first_queryset_dict[item['id']] = item
        for item in to_list:
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
            item['user__icon'] = "%s://%s%s%s" % (
            request.scheme, request.META['HTTP_HOST'], settings.MEDIA_URL, item['user__icon'])
            first_queryset_dict[item['root']]['child'].append(item)

        first_queryset_list=[]
        for item in first_queryset_dict.values():
            first_queryset_list.append(item)
        return first_queryset_list



class SoftwareReleaseAddModelSerializer(serializers.ModelSerializer):
    """
    需要传：
        插件名称
        插件标签
        插件简介
        插件版本
        更新说明
        插件说明
        付费形式
        源码文件
        人民币
        美元
        插件作者

    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = models.Software
        # fields = ['id','name','brief','rnb','dollar','user','check','release_form']
        fields = "__all__"



class SoftwareReleaseUpdateModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Software
        fields = ['id','name','source_code_file','direction_markdown_text']
        extra_kwargs = {
            'name':{'read_only':True}
        }



class CommentSoftGetModelSerializer(serializers.ModelSerializer):
    user__nickname = serializers.CharField(source="user.nickname",read_only=True)
    user__icon = serializers.ImageField(source='user.icon',read_only=True)
    reply_id = serializers.IntegerField(source="reply.id",read_only=True)
    reply__user__nickname = serializers.CharField(source='reply.user.nickname',read_only=True)
    create_time=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updata_time=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = models.Comment_soft
        exclude = ['article','user','root']

class CommentSoftPostModelSerializer(serializers.ModelSerializer):
    """
    插件详情用户创建评论序列化类
    """
    user__nickname = serializers.CharField(source="user.nickname", read_only=True)
    user__icon = serializers.ImageField(source='user.icon', read_only=True)
    user__id = serializers.CharField(source='user.pk', read_only=True)
    # reply_id = serializers.IntegerField(source="reply.id", read_only=True)
    reply__user__nickname = serializers.CharField(source='reply.user.nickname', read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model=models.Comment_soft
        exclude = ['user']



class MyPublishPluginsListModelSerializer(serializers.ModelSerializer):
    """
    我发布的插件列表序列化类
    """

    tab = serializers.SerializerMethodField()
    check = serializers.CharField(source="get_check_dispaly",read_only=True)
    class Meta:
        model = models.Software
        fields = ['id','name','brief','rnb','dollar','create_time','updata_time','tab','check','earnings','direction_markdown_text']

    def get_tab(self,obj):
        tab_queyset = models.Tab.objects.filter(software = obj).values('tab_name')
        return tab_queyset

class MyPublishPluginsDetailModelSerializer(serializers.ModelSerializer):
    """
    插件详情
    """
    tab = serializers.SerializerMethodField()
    versions = serializers.SerializerMethodField()
    class Meta:
        model = models.Software
        fields = ['tab','versions','affiliation','currency','name','brief','source_code_file','direction_for_use','rnb','dollar','check','release_form','direction_markdown_text']
    def get_tab(self,obj):
        tab_queyset = models.Tab.objects.filter(software = obj).values('tab_name')
        return tab_queyset

    def get_versions(self,obj):
        versions_list = []
        versions_queyset = models.Versions.objects.filter(software=obj).values('version','plugin_instructions','version_type')
        for item in versions_queyset:
            versions_list.append(item)
        return versions_list


    def update(self, instance, validated_data):
        instance.affiliation=self.instance.affiliation
        instance.currency = validated_data.get('currency',self.instance.currency)
        instance.name = validated_data.get('name',self.instance.name)
        instance.brief = validated_data.get('brief',self.instance.brief)
        instance.source_code_file = validated_data.get('source_code_file',self.instance.source_code_file)
        instance.direction_for_use = validated_data.get('direction_for_use',self.instance.direction_for_use)
        instance.rnb = validated_data.get('rnb',self.instance.rnb)
        instance.dollar = validated_data.get('dollar',self.instance.dollar)
        instance.check = 0
        instance.putaway = False
        instance.release_form = validated_data.get('release_form',self.instance.release_form)
        instance.version_type = validated_data.get('version_type',self.instance.version_type)
        instance.save()
        return instance
class RedactSoftwarePutModelSerializer(serializers.ModelSerializer):
    """
    个人编辑插件:
    """
    tab = serializers.SerializerMethodField()
    versions = serializers.SerializerMethodField()
    class Meta:
        model = models.Software
        fields = ['release_form','dollar','rnb','direction_for_use','source_code_file','brief','name','currency','affiliation','tab','versions','direction_markdown_text']

    def get_tab(self, obj):
        tab_queyset = models.Tab.objects.filter(software=obj).values('tab_name')
        return tab_queyset

    def get_versions(self, obj):
        versions_list = []
        versions_queyset = models.Versions.objects.filter(software=obj).values('version', 'plugin_instructions',
                                                                               'version_type')
        for item in versions_queyset:
            versions_list.append(item)
        return versions_list
