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
        ('username', u'用户名'),
        ('mobile', u'用户联系方式'),
        ('icon', u'用户头像'),
        ('is_lock', u'是否锁定'),
        ('nickname', u'昵称'),
        ('intro', u'个性签名'),
        ('gender', u'性别'),
        ('create_time', u'创建时间'),
        ('updata_time', u'更新时间'),
        ('is_delete', u'是否删除')
    ])

def en_data_header():
    return dict([
        ('username', u'User Name'),
        ('mobile', u'Mobile'),
        ('icon', u'Icon'),
        ('is_lock', u'Is Lock'),
        ('nickname', u'Nick Name'),
        ('intro', u'Personalized Signature'),
        ('gender', u'Gender'),
        ('create_time', u'Create Time'),
        ('updata_time', u'Update Time'),
        ('is_delete', u'Is Delete')
    ])





class FileRenderCN(CSVStreamingRenderer):
    header = file_headers()
    labels = cn_data_header()

class FileRenderEN(CSVStreamingRenderer):
    header = file_headers()
    labels = en_data_header()
