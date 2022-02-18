from rest_framework_csv.renderers import CSVStreamingRenderer


def file_headers():
    return [
        'nav_type',
        'darent',
        'methods',
        'name',
        'url',
        'is_external_link',
        'is_show',
        'order',
        'create_time',
        'updata_time',
        'is_delete'
    ]

def cn_data_header():
    return dict([
        ('nav_type', u'导航栏类型'),
        ('darent', u'上级菜单'),
        ('methods', u'请求方式'),
        ('name', u'导航名称'),
        ('url', u'路由地址'),
        ('is_external_link', u'是否是外链'),
        ('is_show', u'是否展示'),
        ('order', u'排序优先等级'),
        ('create_time', u'创建时间'),
        ('updata_time', u'更新时间'),
        ('is_delete', u'是否删除')
    ])

def en_data_header():
    return dict([
        ('nav_type', u'Navigation Bar Type'),
        ('darent', u'Superior Navigation Bar'),
        ('methods', u'Request Method'),
        ('name', u'Navigation Bar Name'),
        ('url', u'Aroute'),
        ('is_external_link', u'Is It External Chain'),
        ('is_show', u'Whether To Show'),
        ('order', u'Sorting level'),
        ('create_time', u'Create Time'),
        ('updata_time', u'Updata Time'),
        ('is_delete', u'Is Delete')
    ])





class FileRenderCN(CSVStreamingRenderer):
    header = file_headers()
    labels = cn_data_header()

class FileRenderEN(CSVStreamingRenderer):
    header = file_headers()
    labels = en_data_header()
