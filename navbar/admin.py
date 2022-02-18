from django.contrib import admin

# Register your models here.
from . import models

# admin.site.register(models.Navbar)

@admin.register(models.Navbar)
class Navbar(admin.ModelAdmin):

    list_display =('id','nav_type','darent','methods','name','url','is_external_link','is_show','order','create_time')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('nav_type','darent','methods','name','url','is_external_link','is_show','order','create_time')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id',)
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)