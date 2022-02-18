from rest_framework_csv.renderers import CSVStreamingRenderer


def file_headers():
    return [
        'you_name',
        'you_email',
        'you_email',
        'leave_word',
        'create_time',
        'updata_time',
        'is_delete'
    ]

def cn_data_header():
    return dict([
        ('you_name', u'您的名字'),
        ('you_email', u'您的邮箱'),
        ('you_company', u'您的企业'),
        ('leave_word', u'给我们留言'),
        ('create_time', u'创建时间'),
        ('updata_time', u'更新时间'),
        ('is_delete', u'是否删除')
    ])

def en_data_header():
    return dict([
        ('you_name', u'Your Name'),
        ('you_email', u'Your Email Address'),
        ('you_company', u'Your Enterprise'),
        ('leave_word', u'Leave Us A Message'),
        ('create_time', u'Create Time'),
        ('updata_time', u'Update Time'),
        ('is_delete', u'Is Delate')
    ])





class FileRenderCN(CSVStreamingRenderer):
    header = file_headers()
    labels = cn_data_header()

class FileRenderEN(CSVStreamingRenderer):
    header = file_headers()
    labels = en_data_header()
