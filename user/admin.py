from django.contrib import admin

# Register your models here.


from . import models

# admin.site.register(models.UserInfo)
# admin.site.register(models.Authentication_tab)


admin.site.site_header='GreaterWMS管理后台'
admin.site.site_title = 'GreaterWMS管理后台'
admin.site.index_title = 'GreaterWMS管理后台'


from simpleui.admin import AjaxAdmin


@admin.register(models.UserInfo)
class UserInfo(admin.ModelAdmin):

    list_display =('nickname','intro','email','username','is_superuser','is_staff','user_type','icon','is_lock','authentication_tabs','is_delete')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('nickname','email','is_delete','user_type')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id', 'email', 'username', 'is_delete')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('username','email')


@admin.register(models.Authentication_tab)
class Authentication_tab(admin.ModelAdmin):

    list_display =('email','name','id_number','verify_status','address','sex','is_delete')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('email','name','verify_status','is_delete')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id', 'email', 'name', 'verify_status')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('email','name','verify_status','address','sex')