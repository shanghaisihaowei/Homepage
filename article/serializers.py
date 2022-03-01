from rest_framework import serializers
from . import models

from .models import UserInfo
from pyquery import PyQuery as pq

from rest_framework.exceptions import APIException
import re
from django.conf import settings
import django.utils.timezone as timezone
import base64
import os
import uuid
from PIL import Image
from django.forms import model_to_dict
from comment import models
from bs4 import BeautifulSoup
class ArticleGetModelSerializer(serializers.ModelSerializer):
    author_icon = serializers.SerializerMethodField(read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)

    class Meta:
        model = models.Article
        fields= ['id','title','intro','content','markdown_text','author','language','create_time','updata_time']

    def get_author(self,obj):
        return obj.author.nickname


def Article_validata(data):
    if data is None:
        raise APIException({'detail': '标题不能为空！'})

class ArticleCreateModelSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    class Meta:
        model = models.Article
        fields = ['id', 'title', 'intro', 'content','markdown_text', 'author','language','create_time', 'updata_time']
    extra_kwargs = {
        'title': {'required': True,'validators':[Article_validata]},
    }
    def get_author(self, obj):
        return obj.author.nickname


    def _get_user(self,attrs):
        return attrs

    def _get_intro(self,attrs):
        return attrs

    def _get_cover(self,attrs):
        return attrs

    def _get_language(self,attrs):
        return attrs




class ArticleModelSerializer(serializers.ModelSerializer):
    author_icon = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    changed_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    check_person = serializers.CharField(read_only=True)
    language = serializers.CharField(source="get_language_display",read_only=True)
    comment = serializers.SerializerMethodField()
    class Meta:
        model = models.Article
        fields = ['id','language','check_person', 'title', 'intro', 'content','markdown_text','author_icon','community_type', 'create_time', 'updata_time','changed_time','comment','comment_count']

    extra_kwargs = {
        'title': {'required': True},
    }

    def get_author_icon(self, obj):
        request = self.context.get('request')
        icon_url = "%s://%s%s%s"%(request.scheme,request.META['HTTP_HOST'],settings.MEDIA_URL,obj.author.icon)
        return {"author":obj.author.nickname,"icon":icon_url,'title_tag':obj.author.user_type}

    def get_comment(self,obj):
        """
        获取所有一级评论
        :param obj:
        :return:
        """
        first_queryset = models.Comment_sheet.objects.filter(article=obj,is_delete=False,root=None).order_by('-id').values(
            'id',
            'content',
            'user__id',
            'user__icon',
            'user__nickname',
            'create_time',
            'article',
            'root',
            'is_author',
        )
        queryset_id = models.Comment_sheet.objects.filter(article=obj, is_delete=False, root=None).order_by(
            '-id').values(
            'id',
        )
        id_list = []
        for item in queryset_id:
            id_list.append(item['id'])
        to_list=models.Comment_sheet.objects.filter(article=obj, is_delete=False, root__in=id_list).order_by(
            '-id').values(
            'id',
            'content',
            'user__id',
            'user__icon',
            'user__nickname',
            'create_time',
            'article',
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
        # first_queryset = models.Comment_sheet.objects.filter(article=obj,depth=1,is_delete=False).order_by('id')[0:10].values(
        #     'id',
        #     'content',
        #     'depth',
        #     'user__id',
        #     'user__nickname',
        #     'user__icon',
        #     'create_time',
        #     'article',
        # )
        # first_id_list = []
        # for item in first_queryset:
        #     first_id_list.append(item['id'])
        #
        # from django.db.models import Max
        #
        # result = models.Comment_sheet.objects.filter(article=obj,depth=2,reply_id__in=first_id_list,check_person = 1).values('reply_id').annotate(max_id=Max('id'))
        # second_id_list = [item['max_id'] for item in result]
        #
        # second_queryset = models.Comment_sheet.objects.filter(id__in=second_id_list,is_delete=False).values(
        #     'id',
        #     'content',
        #     'depth',
        #     'user__id',
        #     'user__nickname',
        #     'user__icon',
        #     'create_time',
        #     'reply_id',
        #     'reply__user__nickname',
        #     'article',
        # )
        # import collections
        # first_dict = collections.OrderedDict() # 有序字典
        # request = self.context.get('request')
        # for item in first_queryset:
        #     item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
        #     item['user__icon'] = "%s://%s%s%s"%(request.scheme,request.META['HTTP_HOST'],settings.MEDIA_URL,item['user__icon'])
        #     first_dict[item['id']] = item
        #
        # for node in second_queryset:
        #     node['create_time'] = node['create_time'].strftime('%Y-%m-%d %H:%M')
        #     first_dict[node['reply_id']]['child'] = [node,]
        #
        # return first_dict.values()


    def validate(self, attrs):
        content_html=attrs.get('content')
        dr = re.compile(r'<[^>]+>', re.S)
        content = dr.sub('', content_html)
        print(content)
        # content.replace('<img ','<img style="width:100%"')
        reg = re.compile('.*src=\"(data:image/*?)\"')
        # print(reg)
        # if re.match(reg, content_html):
        #     m1 = reg.findall(content_html)
        #     attrs['cover']=m1[0].replace('http://127.0.0.1:8000/media/','')
        #     print(m1[0])
        # else:
        #     attrs['cover'] = None
        if len(content)>200:
            attrs['intro']=content[:200]
        else:
            attrs['intro']=content
        return attrs

    def create(self, validated_data):
        user=self.context['request'].user.pk
        lang = self.context['request'].META.get('HTTP_LANGUAGE')

        if lang == 'zh-hans':
            author = models.UserInfo.objects.filter(pk=user).first()
            article = models.Article.objects.create(author=author, title=validated_data['title'],
                                                    intro=validated_data['intro'],
                                                    content=validated_data['content'],
                                                    # cover=validated_data['cover'],
                                                    markdown_text=validated_data['markdown_text'],
                                                    language=0)
            article.save()
            return article
        else:
            author=models.UserInfo.objects.filter(pk=user).first()
            article=models.Article.objects.create(author=author,
                                                  title=validated_data['title'],
                                                  intro=validated_data['intro'],
                                                  content=validated_data['content'],
                                                  # cover=validated_data['cover'],
                                                  markdown_text=validated_data['markdown_text'],
                                                  language=1
                                                  )
            article.save()
            return article


    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.intro = validated_data['intro']
        instance.content = validated_data['content']
        instance.markdown_text = validated_data['markdown_text']
        instance.save()
        return instance


class ArticleAddModelSerializer(serializers.ModelSerializer):
    author_icon = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    changed_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    check_person = serializers.CharField(read_only=True)
    language = serializers.CharField(source="get_language_display",read_only=True)
    class Meta:
        model = models.Article
        fields = ['id','language', 'check_person','title', 'intro', 'content','markdown_text', 'author_icon', 'community_type','create_time', 'updata_time','changed_time']
        extra_kwargs = {
            'title': {'required':True},
        }

    def get_author_icon(self, obj):
        request = self.context.get('request')
        icon_url = "%s://%s%s%s"%(request.scheme,request.META['HTTP_HOST'],settings.MEDIA_URL,obj.author.icon)
        return {"author":obj.author.nickname,"icon":icon_url,'title_tag':obj.author.user_type}



    def validate(self, attrs):
        content_html=attrs.get('content',None)
        contents = content_html
        # print(type(content_html))
        # content_html=content_html.replace('<img ','<img style="width:100%" ')
        # print(content_html)
        if content_html is None:  # 内容为空的时候
            attrs['intro'] = None
            attrs['content'] = None
            return attrs
        else:
            content_html = BeautifulSoup(content_html, 'html.parser')
            tags = content_html.find_all()
            for i in tags:
                if i.name == 'script':  # 去除script标签
                    i.decompose()
            dr = re.compile(r'<[^>]+>', re.S)
            content = dr.sub('',str(content_html))  # 提取简介
            content_html=str(content_html)
            # content_html = content_html.replace('<img ', '<img style="width:100%" ')
            attrs['content'] = contents
            if len(content) > 200:
                attrs['intro'] = content[:200]   # 有简介
                return attrs
            else:
                attrs['intro'] = content
                return attrs

    def create(self, validated_data):
        user=self.context['request'].user.pk
        lang = self.context['request'].META.get('HTTP_LANGUAGE')

        if lang == 'zh-hans':
            author = models.UserInfo.objects.filter(pk=user).first()
            article = models.Article.objects.create(author=author, title=validated_data['title'],
                                                    intro=validated_data['intro'],
                                                    content=validated_data['content'],
                                                    # is_cover=validated_data['is_cover'],
                                                    # cover=validated_data['cover'],
                                                    language=0,
                                                    community_type=validated_data['community_type'],
                                                    markdown_text=validated_data['markdown_text'],
                                                    changed_time=timezone.now())
            article.save()
            return article
        else:
            author = models.UserInfo.objects.filter(pk=user).first()
            article = models.Article.objects.create(author=author,
                                                    title=validated_data['title'],
                                                    intro=validated_data['intro'],
                                                    content=validated_data['content'],
                                                    # is_cover=validated_data['is_cover'],
                                                    # cover=validated_data['cover'],
                                                    language=1,
                                                    community_type=validated_data['community_type'],
                                                    markdown_text=validated_data['markdown_text'],
                                                    changed_time=timezone.now())
            article.save()
            return article

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.intro = validated_data['intro']
        # instance.cover = validated_data['cover'],
        # instance.is_cover=validated_data['is_cover']
        instance.content = validated_data['content']
        instance.markdown_text=validated_data['markdown_text']
        instance.check_person = 2
        instance.changed_time=timezone.now()
        instance.save()
        return instance


class BrowseArticleModelSerializer(serializers.ModelSerializer):
    author_icon = serializers.SerializerMethodField(read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    check_person = serializers.CharField(source="get_check_person_display")
    changed_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    # user = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    class Meta:
        model = models.Article
        fields = ['id','check_person', 'title', 'intro', 'markdown_text','author_icon','community_type', 'create_time', 'updata_time','changed_time','comment','comment_count']

    # def get_user(self,obj):
    #     return model_to_dict(obj.author, fields=['id', 'nickname', 'icon'])
    def get_author_icon(self, obj):
        request = self.context.get('request')
        icon_url = "%s://%s%s%s"%(request.scheme,request.META['HTTP_HOST'],settings.MEDIA_URL,obj.author.icon)
        return {"id":obj.author.id,"author":obj.author.nickname,"icon":icon_url,'title_tag':obj.author.user_type}

    def get_comment(self, obj):
        """
        获取所有一级评论
        :param obj:
        :return:
        """
        first_queryset = models.Comment_sheet.objects.filter(article=obj, is_delete=False, root=None).order_by(
            '-id').values(
            'id',
            'content',
            'user__id',
            'user__icon',
            'user__nickname',
            'create_time',
            'article',
            'root',
            'is_author',
        )
        queryset_id = models.Comment_sheet.objects.filter(article=obj, is_delete=False, root=None).order_by(
            '-id').values(
            'id',
        )
        id_list = []
        for item in queryset_id:
            id_list.append(item['id'])
        to_list = models.Comment_sheet.objects.filter(article=obj, is_delete=False, root__in=id_list).order_by(
            '-id').values(
            'id',
            'content',
            'user__id',
            'user__icon',
            'user__nickname',
            'create_time',
            'article',
            'root',
            'reply',
            'reply__user__nickname',
            'is_author',
        )

        request = self.context.get('request')
        for item in first_queryset:
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
            item['user__icon'] = "%s://%s%s%s" % (
            request.scheme, request.META['HTTP_HOST'], settings.MEDIA_URL, item['user__icon'])
            item['child'] = []
        first_queryset_dict = {}

        for item in first_queryset:
            first_queryset_dict[item['id']] = item
        for item in to_list:
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
            item['user__icon'] = "%s://%s%s%s" % (
                request.scheme, request.META['HTTP_HOST'], settings.MEDIA_URL, item['user__icon'])
            first_queryset_dict[item['root']]['child'].append(item)

        first_queryset_list = []
        for item in first_queryset_dict.values():
            first_queryset_list.append(item)
        return first_queryset_list


class BrowseArticleDetailModelSerializer(serializers.ModelSerializer):
    author_icon = serializers.SerializerMethodField(read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    check_person = serializers.CharField(source="get_check_person_display")
    changed_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M",read_only=True)
    # user = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    class Meta:
        model = models.Article
        fields = ['id','check_person', 'title', 'intro','markdown_text', 'content', 'author_icon','community_type', 'create_time', 'updata_time','changed_time','comment','comment_count']

    # def get_user(self,obj):
    #     return model_to_dict(obj.author, fields=['id', 'nickname', 'icon'])
    def get_author_icon(self, obj):
        request = self.context.get('request')
        icon_url = "%s://%s%s%s"%(request.scheme,request.META['HTTP_HOST'],settings.MEDIA_URL,obj.author.icon)
        return {"id":obj.author.id,"author":obj.author.nickname,"icon":icon_url,'title_tag':obj.author.user_type}

    def get_comment(self, obj):
        """
        获取所有一级评论
        :param obj:
        :return:
        """
        first_queryset = models.Comment_sheet.objects.filter(article=obj, is_delete=False, root=None).order_by(
            '-id').values(
            'id',
            'content',
            'user__id',
            'user__icon',
            'user__nickname',
            'create_time',
            'article',
            'root',
            'is_author',
        )
        queryset_id = models.Comment_sheet.objects.filter(article=obj, is_delete=False, root=None).order_by(
            '-id').values(
            'id',
        )
        id_list = []
        for item in queryset_id:
            id_list.append(item['id'])
        to_list = models.Comment_sheet.objects.filter(article=obj, is_delete=False, root__in=id_list).order_by(
            '-id').values(
            'id',
            'content',
            'user__id',
            'user__icon',
            'user__nickname',
            'create_time',
            'article',
            'root',
            'reply',
            'reply__user__nickname',
            'is_author',
        )

        request = self.context.get('request')
        for item in first_queryset:
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
            item['user__icon'] = "%s://%s%s%s" % (
            request.scheme, request.META['HTTP_HOST'], settings.MEDIA_URL, item['user__icon'])
            item['child'] = []
        first_queryset_dict = {}

        for item in first_queryset:
            first_queryset_dict[item['id']] = item
        for item in to_list:
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
            item['user__icon'] = "%s://%s%s%s" % (
                request.scheme, request.META['HTTP_HOST'], settings.MEDIA_URL, item['user__icon'])
            first_queryset_dict[item['root']]['child'].append(item)

        first_queryset_list = []
        for item in first_queryset_dict.values():
            first_queryset_list.append(item)
        return first_queryset_list
    # def get_comment(self,obj):
    #     """
    #     获取所有一级评论
    #     :param obj:
    #     :return:
    #     """
    #     first_queryset = models.Comment_sheet.objects.filter(article=obj,depth=1,is_delete=False).order_by('-id')[0:10].values(
    #         'id',
    #         'content',
    #         'depth',
    #         'user__id',
    #         'user__nickname',
    #         'user__icon',
    #         'create_time',
    #         'article'
    #     )
    #     first_id_list = []
    #     for item in first_queryset:
    #         first_id_list.append(item['id'])
    #
    #     from django.db.models import Max
    #     # 获取二级评论
    #     result = models.Comment_sheet.objects.filter(article=obj,depth=2,reply_id__in=first_id_list,is_delete=False).values('reply_id').annotate(max_id=Max('id'))
    #     second_id_list = [item['max_id'] for item in result]
    #
    #     second_queryset = models.Comment_sheet.objects.filter(id__in=second_id_list,is_delete=False).values(
    #         'id',
    #         'content',
    #         'depth',
    #         'user__nickname',
    #         'user__icon',
    #         'create_time',
    #         'reply_id',
    #         'reply__user__nickname',
    #         'article',
    #     )
    #     import collections
    #     first_dict = collections.OrderedDict() # 有序字典
    #     request = self.context.get('request')
    #     for item in first_queryset:
    #         item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
    #         item['user__icon'] = "%s://%s%s%s"%(request.scheme,request.META['HTTP_HOST'],settings.MEDIA_URL,item['user__icon'])
    #         first_dict[item['id']] = item
    #
    #     for node in second_queryset:
    #         node['create_time'] = node['create_time'].strftime('%Y-%m-%d %H:%M')
    #         node['user__icon'] = "%s://%s%s%s"%(request.scheme,request.META['HTTP_HOST'],settings.MEDIA_URL,node['user__icon'])
    #         first_dict[node['reply_id']]['child'] = [node,]
    #
    #     return first_dict.values()




class TopArticleViewModelSerializer(serializers.ModelSerializer):
    author_icon = serializers.SerializerMethodField(read_only=True)
    changed_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    class Meta:
        model = models.Article
        fields = ['id','title','intro','author_icon','language','changed_time','create_time','updata_time','top']
    def get_author_icon(self, obj):
        request = self.context.get('request')
        # icon_url = "%s://%s%s%s" % (request.scheme, request.META['HTTP_HOST'], settings.MEDIA_URL, obj.author.icon)
        return {"id": obj.author.id, "author": obj.author.nickname, 'title_tag': obj.author.user_type}

class TopArticleViewDetailModelSerializer(serializers.ModelSerializer):
    author_icon = serializers.SerializerMethodField(read_only=True)
    changed_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updata_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    comment = serializers.SerializerMethodField()
    class Meta:
        model = models.Article
        fields = ['id','title','intro','comment','content','author_icon','check_person','language','changed_time','create_time','updata_time','community_type','comment_count','top']

    def get_author_icon(self, obj):
        request = self.context.get('request')
        icon_url = "%s://%s%s%s" % (request.scheme, request.META['HTTP_HOST'], settings.MEDIA_URL, obj.author.icon)
        return {"id": obj.author.id, "author": obj.author.nickname, "icon": icon_url, 'title_tag': obj.author.user_type}

    def get_comment(self, obj):
        """
        获取所有一级评论
        :param obj:
        :return:
        """
        first_queryset = models.Comment_sheet.objects.filter(article=obj, is_delete=False, root=None).order_by(
            '-id').values(
            'id',
            'content',
            'user__id',
            'user__icon',
            'user__nickname',
            'create_time',
            'article',
            'root',
            'is_author',
        )
        queryset_id = models.Comment_sheet.objects.filter(article=obj, is_delete=False, root=None).order_by(
            '-id').values(
            'id',
        )
        id_list = []
        for item in queryset_id:
            id_list.append(item['id'])
        to_list = models.Comment_sheet.objects.filter(article=obj, is_delete=False, root__in=id_list).order_by(
            '-id').values(
            'id',
            'content',
            'user__id',
            'user__icon',
            'user__nickname',
            'create_time',
            'article',
            'root',
            'reply',
            'reply__user__nickname',
            'is_author',
        )

        request = self.context.get('request')
        for item in first_queryset:
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
            item['user__icon'] = "%s://%s%s%s" % (
                request.scheme, request.META['HTTP_HOST'], settings.MEDIA_URL, item['user__icon'])
            item['child'] = []
        first_queryset_dict = {}

        for item in first_queryset:
            first_queryset_dict[item['id']] = item
        for item in to_list:
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
            item['user__icon'] = "%s://%s%s%s" % (
                request.scheme, request.META['HTTP_HOST'], settings.MEDIA_URL, item['user__icon'])
            first_queryset_dict[item['root']]['child'].append(item)

        first_queryset_list = []
        for item in first_queryset_dict.values():
            first_queryset_list.append(item)
        return first_queryset_list