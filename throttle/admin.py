from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.ListModel)
class ListModel(admin.ModelAdmin):

    list_display =('ip','method','t_code','create_time')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('ip','method','t_code','create_time')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id', 'ip', 'method', 't_code','create_time')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('ip','method','create_time')