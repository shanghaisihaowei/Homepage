
from rest_framework import serializers
from . import models
import re
from rest_framework.exceptions import ValidationError

from .models import Comment_sheet
from .models import UserInfo

class CommentGetModelSerializer(serializers.ModelSerializer):
    user__nickname = serializers.CharField(source="user.nickname",read_only=True)
    user__icon = serializers.ImageField(source='user.icon',read_only=True)
    reply_id = serializers.IntegerField(source="reply.id",read_only=True)
    reply__user__nickname = serializers.CharField(source='reply.user.nickname',read_only=True)
    create_time=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updata_time=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = Comment_sheet
        exclude = ['article','user','reply','root']


class CommentPostModelSerializer(serializers.ModelSerializer):
    user__nickname = serializers.CharField(source="user.nickname",read_only=True)
    user__icon = serializers.ImageField(source='user.icon',read_only=True)
    user__id = serializers.CharField(source='user.pk', read_only=True)
    # reply_id = serializers.IntegerField(source="reply.id",read_only=True)
    reply__user__nickname = serializers.CharField(source='reply.user.nickname',read_only=True)
    create_time=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updata_time=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = Comment_sheet
        exclude = ['user']











