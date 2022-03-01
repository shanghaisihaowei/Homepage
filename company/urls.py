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


''' SimpleRouter用于注册路由 '''
from . import views
from rest_framework import routers



urlpatterns = [
    path(r'resp/',views.Stream_video_View.as_view({'get':'stream_video'})),
    path(r'banner/',views.HomeBannerlistview.as_view({'get':'list'})),
    path(r'article_banner/',views.ArticleBannerView.as_view({'get':'list'})),
    path(r'mobile_banner/',views.MobileArticleBannerView.as_view({'get':'list'})),
    path(r'recorder/',views.RecorderlistView.as_view({'get':'list'})),

]
