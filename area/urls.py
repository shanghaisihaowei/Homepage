from django.urls import path
from . import views

urlpatterns = [
path(r'', views.APIViewSet.as_view({"get": "list", "post": "create"}), name="area"),
path('check/', views.Area_Check.as_view(), name="area_check"),
]
