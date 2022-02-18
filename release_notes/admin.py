from django.contrib import admin

# Register your models here.


from . import models


# admin.site.register(models.Timer_shaft)
# admin.site.register(models.Details)


@admin.register(models.Timer_shaft)
class Timer_shaft(admin.ModelAdmin):

    list_display =('id','versions','language','title','iteration_time','node')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('versions','title','node','language')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id', 'language')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)


@admin.register(models.Details)
class Details(admin.ModelAdmin):

    list_display =('id','timer_shaft','content','language')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('timer_shaft','content','language')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id', 'language')
    # 按发布日期降序排序
    ordering = ('id',)
    # 搜索条件设置
    search_fields = ('id',)