from rest_framework_csv.renderers import CSVStreamingRenderer

def file_headers():
    return [
        'title',
        'intro',
        # 'cover',
        'content',
        'author',
        'check_person',
        'create_time',
        'updata_time',
        'is_delete'
    ]

def cn_data_header():
    return dict([
        ('title', u'文章标题'),
        ('intro', u'文章简介'),
        # ('cover', u'文章封面'),
        ('content', u'文章内容'),
        ('author', u'文章作者'),
        ('check_person', u'文章审核状态'),
        ('create_time', u'创建时间'),
        ('updata_time', u'最后更新时间'),
        ('is_delete', u'是否删除')
    ])

def en_data_header():
    return dict([
        ('title', u'Article Title'),
        ('intro', u'Introduce'),
        # ('cover', u'Article Covers'),
        ('content', u'Contents Of Article'),
        ('author', u'Article Author'),
        ('check_person', u'Verifier'),
        ('create_time', u'Create Time'),
        ('updata_time', u'Update Time'),
        ('is_delete', u'Whether To Remove'),
    ])

class FileRenderCN(CSVStreamingRenderer):
    header = file_headers()
    labels = cn_data_header()

class FileRenderEN(CSVStreamingRenderer):
    header = file_headers()
    labels = en_data_header()
