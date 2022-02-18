from django.contrib import admin

# Register your models here.


from . import models

# admin.site.register(models.Tab)
# admin.site.register(models.Software)
# admin.site.register(models.Versions)


from . import models


@admin.register(models.Tab)
class Tab(admin.ModelAdmin):

    list_display =('id','tab_name','software','is_delete','create_time')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('tab_name','software','is_delete','create_time')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id', 'tab_name', 'software','create_time')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('tab_name','software','create_time')



@admin.register(models.Software)
class Software(admin.ModelAdmin):

    list_display =('id','affiliation','name','user','check','putaway','currency','people_buy','number_downloads','earnings')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('affiliation','name','check','putaway')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id', 'affiliation', 'name','check','putaway','create_time')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('affiliation','name','create_time')



@admin.register(models.Versions)
class Versions(admin.ModelAdmin):

    list_display =('id','version_type','version','software')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('version_type','version','software')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id', 'version_type')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)


@admin.register(models.Comment_soft)
class Comment_soft(admin.ModelAdmin):

    list_display =('id','user','softwares','softwares','check_person','root','reply','is_author')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('user','softwares','softwares','check_person')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id', 'check_person')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)