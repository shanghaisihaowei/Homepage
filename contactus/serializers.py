
from rest_framework import serializers
from . import models
import re
from rest_framework.exceptions import ValidationError

from celery_task.user_feedback import send_company_feedback

class ContactModelSerializer(serializers.ModelSerializer):
    options = serializers.IntegerField()
    class Meta:
        model = models.Contact
        fields = ['your_name','your_email','leave_word','your_phone','options']
        extra_kwargs ={
            'your_name':{'required':True,'write_only':True},
            'your_email':{'required':True,'write_only':True},
            'leave_word':{'required':True,'write_only':True},
            'your_phone':{'required':True,'write_only':True},
            'options':{'required':True,'write_only':True}
        }







