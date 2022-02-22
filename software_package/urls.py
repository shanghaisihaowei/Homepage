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

router = routers.SimpleRouter()

# router.register('software',views.SoftwareReleaseGetView,basename="software")

urlpatterns = [
    path('softwareget/',views.SoftwareReleaseGetView.as_view({'get':'list'})),
    path('softwaregetret/<int:id>/',views.SoftwareReleaseGetView.as_view({'get':'retrieve'})),
    path('add/',views.SoftwareReleaseAddView.as_view({'post':'create'})),
    path('add/<int:id>/',views.SoftwareReleaseAddView.as_view({'put':'update'})),
    path('downzip/<int:id>/',views.DownLoadZipFile.as_view()),
    path('comment/',views.CommentCreateView.as_view({'post':'create'})),
    path('my_soft/', views.MySoftwareReleaseGetView.as_view({'get': 'list'})),
    path('my_soft/<int:id>/', views.MySoftwareReleaseGetView.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update',})),
    path('banner_soft/',views.Bannerlistview.as_view({'get':'list'})),
]
urlpatterns+=router.urls

