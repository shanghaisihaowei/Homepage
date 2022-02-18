from django.contrib import admin

# Register your models here.
from . import models
# admin.site.register(models.Withdrawal_instructions)
# admin.site.register(models.Rmb_ccount)
# admin.site.register(models.Rmb_wallet)
# admin.site.register(models.Rmb_salary_detail)
# admin.site.register(models.Withdrawal_details)
# admin.site.register(models.Dollar_wallet)
# admin.site.register(models.Dollar_salary_detail)
# admin.site.register(models.Dollar_withdrawal_details)
# admin.site.register(models.Account_bank)
# admin.site.register(models.Usd_account)





from . import models
@admin.register(models.Withdrawal_instructions)
class Withdrawal_instructions(admin.ModelAdmin):

    list_display =('id','content','is_show','create_time','updata_time','is_delete')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('content','is_show','create_time','updata_time','is_delete')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id',)
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)


@admin.register(models.Rmb_ccount)
class Rmb_ccount(admin.ModelAdmin):

    list_display =('id','users','alipay_account','account_holder','account_type','is_default','is_delete')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('users','alipay_account','account_holder','account_type','is_default','is_delete')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id',)
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id','users',)


@admin.register(models.Rmb_wallet)
class Rmb_wallet(admin.ModelAdmin):

    list_display =('id','userinfos','balance','withdrawal_amount','Platform_extraction_rate','updata_time')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('userinfos','balance','withdrawal_amount','Platform_extraction_rate','updata_time')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id',)
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id','userinfos',)

@admin.register(models.Rmb_salary_detail)
class Rmb_salary_detail(admin.ModelAdmin):

    list_display =('id','user','email','title','total','author','create_time')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('user','email','title','total','author','create_time')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id',)
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id','email',)






@admin.register(models.Withdrawal_details)
class Withdrawal_details(admin.ModelAdmin):

    list_display =('id','user','balance','withdrawal_type','Amount_of_money','alipay_account','verify_status','create_time')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('user','balance','withdrawal_type','Amount_of_money','alipay_account','verify_status','create_time')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id',)
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id','verify_status',)





@admin.register(models.Dollar_wallet)
class Dollar_wallet(admin.ModelAdmin):

    list_display =('id','userinfos','balance','withdrawal_amount','Platform_extraction_rate')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('userinfos','balance','withdrawal_amount','Platform_extraction_rate')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id',)
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)


@admin.register(models.Dollar_salary_detail)
class Dollar_salary_detail(admin.ModelAdmin):

    list_display =('id','user','email','title','total','author','create_time')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('user','email','title','total','author','create_time')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id',)
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)

@admin.register(models.Dollar_withdrawal_details)
class Dollar_withdrawal_details(admin.ModelAdmin):

    list_display =('id','users','balance','withdrawal_type','Amount_of_money','paypal_account','verify_status')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('users','balance','withdrawal_type','Amount_of_money','paypal_account','verify_status')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id','verify_status',)
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)


@admin.register(models.Account_bank)
class Account_bank(admin.ModelAdmin):

    list_display =('id','users','name','id_number','is_default','verify_status','create_time')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('users','name','id_number','is_default','verify_status','create_time')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id','verify_status',)
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)




@admin.register(models.Usd_account)
class Usd_account(admin.ModelAdmin):

    list_display =('id','users','account_number','account_type','is_default','verify_status','create_time')
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('users','account_number','account_type','is_default','verify_status','create_time')
    # 每页显示条目数 缺省值100
    list_per_page = 10
    readonly_fields = ('id',)
    # 设置过滤选项
    list_filter = ('id','verify_status',)
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)

