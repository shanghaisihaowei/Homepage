from django.contrib import admin

# Register your models here.

from . import models
@admin.register(models.MarketUpload)
class MarketUpload(admin.ModelAdmin):

    list_display =('id','imge','is_show','create_time','is_delete')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('imge','is_show','create_time','is_delete')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id',)
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)


@admin.register(models.HomeBanner)
class HomeBanner(admin.ModelAdmin):

    list_display =('id','title','is_delete','is_show','orders','created_time')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('title','is_delete','is_show','orders')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id',)
    # 按发布日期降序排序
    ordering = ('-created_time',)
    # 搜索条件设置
    search_fields = ('id',)

admin.site.register(models.Recorder)