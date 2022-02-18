from django.contrib import admin

# Register your models here.


from . import models

# admin.site.register(models.Contact)
# admin.site.register(models.Staffemail)


from . import models
@admin.register(models.Contact)
class Contact(admin.ModelAdmin):

    list_display =('id','your_name','your_email','leave_word','your_phone','options')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('your_name','your_email','leave_word','your_phone','options')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id',)
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)



