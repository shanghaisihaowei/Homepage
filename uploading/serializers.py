from rest_framework import serializers

from django.conf import settings
from rest_framework.exceptions import ValidationError
import re
from .models import Uploading
from utils.HomePage_logging import get_logger



class UploadingGetModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = Uploading
        fields = ['id','barcode_scanner','mac','win','android']

