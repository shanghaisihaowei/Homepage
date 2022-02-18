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
from . import views
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register('',views.NavbarView)
from rest_framework import routers

router = routers.SimpleRouter()

# router.register('details',views.DetailsView,basename="details")
# router.register('timer_shaft',views.Timer_shaftView,basename="timer_shaft")


urlpatterns = [
    path("order/",views.OrderAddView.as_view({"post":"create"})),
    path('wx_pay/', views.Wx.as_view()),  # 支付页面
    path('notify/', views.NotifyView.as_view()),# 回调地址
    path('wx_back/', views.WxBack.as_view()),  # 查单地址
    path('zfb_pay/', views.AlipayView.as_view()),  # 回调地址
    path('zfb_back/', views.PaymentStatusView.as_view()),  # 回调地址
    path('pay_pay/', views.PayPal.as_view()),  # 支付页面
    path('pay_back/', views.PayBack.as_view()),  # 回调地址
    path('check_order/<int:software>/',views.CheckOrder.as_view({'get':'retrieve'})),
    path('check_order/',views.CheckOrder.as_view({'get':'list'})),
    path('order_status/',views.Orderstatus.as_view()),
    path('paystatus/',views.PayStatus.as_view()),
    path('my_order/',views.MyOrder.as_view({'get':'list'})),
    path('trans/', views.AlipayTransView.as_view()),
    path('zfb_order/', views.CheckPayView.as_view()),
    re_path(r'^my_order/(?P<order_id>\d+)/$', views.MyOrder.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    }))

]
urlpatterns +=router.urls