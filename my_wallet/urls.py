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


urlpatterns = [
    path('explain/',views.Withdrawal_InstructionsView.as_view({'get':'list'})),
    path('r_wallet/',views.Rmb_walletView.as_view({'get':'list'})),
    path('d_wallet/',views.Dollar_walletView.as_view({'get':'list'})),
    path('rmb_salary/',views.Rmb_salary_detailView.as_view({'get':'list'})),
    path('dollar_salary/',views.Dollar_salary_detailView.as_view({'get':'list'})),
    path('r_account/',views.Account_bankView.as_view({'get':'list'})),
    path('rnbccount/',views.RmbCcountView.as_view({'get':'list','post':'create'})),
    path('rnbccount/<int:id>/',views.RmbCcountView.as_view({'delete':'destroy','put':'update'})),
    path('usd_account/',views.Usd_accountView.as_view({'get':'list','post':'create'})),
    path('usd_account/<int:id>/',views.Usd_accountView.as_view({'delete':'destroy','put':'update'})),
    path('r_cash/',views.Withdrawal_detailsView.as_view({'get':'list','post':'create'})),
    path('d_cash/',views.Dollar_withdrawal_detailsView.as_view({'get':'list','post':'create'})),
]
urlpatterns +=router.urls