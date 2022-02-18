from django.contrib import admin

# Register your models here.
from . import models
# admin.site.register(models.Order)
# admin.site.register(models.OrderPackage)



@admin.register(models.Order)
class Order(admin.ModelAdmin):

    list_display =('order_id','affiliation','title','status','is_delete','user','total_count','currency','total_amount','pay_type','pay_time','software','payment_id','payerid','create_time')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('status','title','is_delete')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('order_id',)
    # 设置过滤选项
    list_filter = ('order_id','title')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('order_id',)


@admin.register(models.OrderPackage)
class OrderPackage(admin.ModelAdmin):

    list_display =('id','order','software','count','price')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('order','software','count','price')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id', 'order')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)