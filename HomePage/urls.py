from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path,include
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.views import serve
from django.views.static import serve as static_serve
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

def return_static(request, path, insecure=True, **kwargs):
  return serve(request, path, insecure, **kwargs)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="HomePage--API Docs",
        default_version='v1',
        description="这是一个HomePage接口文档",
        terms_of_service="https://www.56yhz.com/",
        # contact=openapi.Contact(email="xxx@qq.com"),
        license=openapi.License(name="Apache License 2.0"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),   # 权限类
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', TemplateView.as_view(template_name='dist/spa/index.html')),
    re_path(r'^favicon\.ico$', views.favicon, name='favicon'),
    re_path('^css/.*$', views.css, name='css'),
    re_path('^js/.*$', views.js, name='js'),
    re_path('^statics/.*$', views.statics, name='statics'),
    re_path('^icons/.*$', views.icons, name='icons'),
    re_path('^fonts/.*$', views.fonts, name='fonts'),
    re_path(r'^static/(?P<path>.*)$', return_static, name='static'),
    re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),

    path('area_v2/', include('area.urls')),
    path('iot/', include('iot.urls')),
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('user/api/v1/',include('user.urls')),
    path('nav/api/v1/',include('navbar.urls')),
    path('article/api/v1/',include('article.urls')),
    path('contact/api/v1/',include('contactus.urls')),
    path('comment/api/v1/',include('comment.urls')),
    path('release/api/v1/',include('release_notes.urls')),
    path('software/api/v1/',include('software_package.urls')),
    path('order/api/v1/',include('order.urls')),
    path('uploadfile/api/v1/',include('uploading.urls')),
    path('pay/api/v1/',include('my_wallet.urls')),
    path('resp/api/v1/',include('company.urls')),

    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.MyTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
urlpatterns += [re_path(r'^silk/', include('silk.urls', namespace='silk'))]