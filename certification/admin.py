from django.contrib import admin

# Register your models here.


from . import models

# admin.site.register(models.Certification)


@admin.register(models.Certification)
class Certification(admin.ModelAdmin):

    list_display =('id','email','name','id_number','audit_status','create_time','updata_time')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('email','name','id_number','audit_status','create_time','updata_time')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id', 'email','audit_status')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)