from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path,include

from . import views

''' SimpleRouter用于注册路由 '''
from rest_framework.routers import SimpleRouter
from rest_framework import routers

router = routers.SimpleRouter()
router.register('userdetail',views.UserDetailView,basename="userdetail")
router.register('userpwd',views.PasswordPutView,basename="userpwd")

urlpatterns = [
    path('get_email/',views.EmailViewSet.as_view({'get': 'get_email'})),
    path('reg_codes/',views.EmailViewSet.as_view({'get': 'reg_codes'})),
    path('login_codes/',views.EmailViewSet.as_view({'get': 'login_codes'})),
    path('pwd_codes/',views.EmailViewSet.as_view({'get': 'pwd_codes'})),
    path('account_codes/',views.EmailViewSet.as_view({'get': 'alipay_codes'})),
    path('reg/',views.RegisterViewSet.as_view({'post': 'reg'})),
    path('login/',views.LoginViewSet.as_view({'post': 'login'})),
    path('code_login/',views.LoginViewSet.as_view({'post': 'code_login'})),
    path('putpwd/',views.PutPwdViewSet.as_view({'post': 'putpwd'})),
    path('auth/',views.AuthenticationView.as_view({'get':'list','post': 'create'})),
    path('auth_status/',views.Auth_status.as_view({'get':'retrieve'})),
    # path('userdetail/',views.UserDetailView.as_view()),
    # path('userupdate/',views.UserDetailUpdateView.as_view()),

]
urlpatterns += router.urls