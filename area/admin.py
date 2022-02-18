from django.contrib import admin
from . models import ListModel



@admin.register(ListModel)
class ListModel(admin.ModelAdmin):

    list_display =('id','ip','iso_code','city','country','continent','detail','create_time','update_time')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('iso_code','city','country','continent','detail','create_time','update_time')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id', 'ip')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)