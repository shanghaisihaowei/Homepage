"""HomePage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path,include

from . import views

''' SimpleRouter用于注册路由 '''
from rest_framework.routers import SimpleRouter
from rest_framework import routers



urlpatterns = [
    # path('getfile/',views.Uploading.as_view({'get': 'list'})),
    # path('addfile/',views.Uploading.as_view({'post': 'create'})),
    # path('delfile/<int:pk>/',views.Uploading.as_view({'delete': 'destroy'})),
    path('uploadfile/',views.Upload_file.as_view({'post': 'create'})),
]
