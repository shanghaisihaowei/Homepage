from django.contrib import admin

# Register your models here.
from . import models
# admin.site.register(models.Article)

@admin.register(models.Article)
class Article(admin.ModelAdmin):

    list_display =('id','community_type','title','author','check_person','language','changed_time','comment_count','create_time','top')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('community_type','title','author','check_person','language','changed_time','comment_count','create_time','top')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id', 'check_person')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)