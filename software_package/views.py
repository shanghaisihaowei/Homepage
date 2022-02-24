from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from . import models

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from utils.page import MyPageNumberPagination
from utils.APIResponse import APIResponse
from . import serializers
from .filter import SoftwareFilter
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.conf import settings
from rest_framework.response import Response
import os
from utils.check_jwt_authenticate import JwtAuth
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.my_permissions import UserPermission
from rest_framework.generics import GenericAPIView
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse
# from . import models
from rest_framework.viewsets import ViewSetMixin
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from order.models import Order
from django.utils.http import urlquote


class SoftwareReleaseGetView(ModelViewSet):
    """
    list:
        Response a data (get)
    retrieve:
        Response a data retrieve（get）
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "people_buy", "create_time", "update_time", ]
    filter_class = SoftwareFilter
    lookup_field = 'id'
    queryset = models.Software.objects.filter().all()
    serializer_class = serializers.SoftwareReleaseGETModelSerializer

    def get_queryset(self):
        return models.Software.objects.filter(check=2,putaway=True)

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.SoftwareReleaseGETModelSerializer
        elif self.action in ['retrieve']:
            return serializers.SoftwareReleaseDetailModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)


class SoftwareReleaseAddView(ModelViewSet):
    """
    create:
        Response a data line (post)
    update:
        Response a data line(put)
    """
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    authentication_classes = (JWTAuthentication, )
#     permission_classes = [UserPermission, ]
    ordering_fields = ['id', "people_buy", "create_time", "update_time", ]
    filter_class = SoftwareFilter
    lookup_field = 'id'
    queryset = models.Software.objects.filter().all()
    serializer_class = serializers.SoftwareReleaseAddModelSerializer

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.SoftwareReleaseAddModelSerializer
        elif self.action in ['update']:
            return serializers.SoftwareReleaseUpdateModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        files = self.request.FILES.get('source_code_file')
        if files is None:
            raise APIException({"detail": "文件不能为空"})
        if files:
            if files.size > 209715200:  # 104857600->100M
                raise APIException({"detail": "文件大小不大于200M"})
            file_type = files.name.split('.')[-1]
            if file_type not in ['zip']:
                raise APIException({"detail": "文件类型必须是zip"})
        data = self.request.data
        user_obj = models.UserInfo.objects.filter(id=request.user.pk).first()
        if data.get('name') is None:
            raise APIException({"detail": "插件名不能为空"})

        # 发布免费插件
        if int(data.get('release_form')) == 0:
            data_dic = {
                'name': data.get("name"),
                'brief': data.get("brief"),
                'rnb': 0,
                'dollar': 0,
                'source_code_file': files,
                'user': self.request.user.pk,
                'release_form': 0,
                'direction_for_use': data.get('direction_for_use'),
                'affiliation':data.get('affiliation'),
                'direction_markdown_text':data.get('direction_markdown_text'),
                'soft_label':user_obj.user_type,
            }

            serializer = self.get_serializer(data=data_dic)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            soft_obj = models.Software.objects.filter(pk=serializer.data['id']).first()
            ver_dic = {
                'version': data.get('version'),
                'plugin_instructions': data.get('plugin_instructions'),
                'software': soft_obj,
                'version_type': data.get('version_type'),
                'plugin_markdown_text':data.get('plugin_markdown_text'),
            }
            models.Versions.objects.create(**ver_dic)
            tab_name = data.get('tab_name')
            if '，' in tab_name:
                tab_list = tab_name.split('，')  # 中文逗号
                for item in tab_list:
                    models.Tab.objects.create(software=soft_obj, tab_name=item)
                return Response(serializer.data)
            elif ',' in tab_name:
                tab_list = tab_name.split(',')  # 英文逗号
                for item in tab_list:
                    models.Tab.objects.create(software=soft_obj, tab_name=item)
                return Response(serializer.data)
            else:  # 没逗号
                models.Tab.objects.create(software=soft_obj, tab_name=tab_name)
            return Response(serializer.data)
        elif int(data.get('release_form')) == 1:
            if int(data.get('currency')) == 0:
                data_dic = {
                    'name': data.get("name"),
                    'brief': data.get('brief'),
                    'rnb': float(data.get('rnb', '0')),
                    'dollar': 0,
                    'source_code_file': files,
                    'user': self.request.user.pk,
                    'release_form': int(data.get('release_form')),
                    'direction_for_use': data.get('direction_for_use'),
                    'currency': data.get('currency'),
                    'affiliation':data.get('affiliation'),
                    'direction_markdown_text':data.get('direction_markdown_text'),
                    'soft_label':user_obj.user_type,
                }
                serializer = self.get_serializer(data=data_dic)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                soft_obj = models.Software.objects.filter(pk=serializer.data['id']).first()
                ver_dic = {
                    'version': data.get('version'),
                    'plugin_instructions': data.get('plugin_instructions'),
                    'software': soft_obj,
                    'version_type':data.get('version_type'),
                    'plugin_markdown_text':data.get('plugin_markdown_text'),
                }
                models.Versions.objects.create(**ver_dic)
                tab_name = data.get('tab_name')
                if '，' in tab_name:
                    tab_list = tab_name.split('，')  # 中文逗号
                    for item in tab_list:
                        models.Tab.objects.create(software=soft_obj, tab_name=item)
                    return Response(serializer.data)
                elif ',' in tab_name:
                    tab_list = tab_name.split(',')  # 英文逗号
                    for item in tab_list:
                        models.Tab.objects.create(software=soft_obj, tab_name=item)
                    return Response(serializer.data)
                else:  # 没逗号
                    models.Tab.objects.create(software=soft_obj, tab_name=tab_name)
                return Response(serializer.data)
            else:
                data_dic = {
                    'name': data.get("name"),
                    'brief': data.get('brief'),
                    'rnb': 0,
                    'dollar': float(data.get('dollar', '0')),
                    'source_code_file': files,
                    'user': self.request.user.pk,
                    'release_form': int(data.get('release_form')),
                    'direction_for_use': data.get('direction_for_use'),
                    'currency': data.get('currency'),
                    'affiliation':data.get('affiliation'),
                    'direction_markdown_text':data.get('direction_markdown_text'),
                    'soft_label': user_obj.user_type,
                }
                serializer = self.get_serializer(data=data_dic)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                soft_obj = models.Software.objects.filter(pk=serializer.data['id']).first()
                ver_dic = {
                    'version': data.get('version'),
                    'plugin_instructions': data.get('plugin_instructions'),
                    'software': soft_obj,
                    'version_type': data.get('version_type'),
                    'plugin_markdown_text':data.get('plugin_markdown_text'),
                }
                models.Versions.objects.create(**ver_dic)
                tab_name = data.get('tab_name')
                if '，' in tab_name:
                    tab_list = tab_name.split('，')  # 中文逗号
                    for item in tab_list:
                        models.Tab.objects.create(software=soft_obj, tab_name=item)
                    return Response(serializer.data)
                elif ',' in tab_name:
                    tab_list = tab_name.split(',')  # 英文逗号
                    for item in tab_list:
                        models.Tab.objects.create(software=soft_obj, tab_name=item)
                    return Response(serializer.data)
                else:  # 没逗号
                    models.Tab.objects.create(software=soft_obj, tab_name=tab_name)
                    return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        files = self.request.FILES.get('source_code_file')
        if files is None:
            raise APIException({"detail": "文件不能为空"})

        if files:
            if files.size > 209715200:  # 104857600->100M
                raise APIException({"detail": "文件大小不大于200M"})
            file_type = files.name.split('.')[1]
            if file_type not in ['zip']:
                raise APIException({"detail": "文件类型必须是zip"})

        updata_dic = {
            'source_code_file': files,
        }
        serializer = self.get_serializer(instance, data=updata_dic, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = request.data
        soft_obj = models.Software.objects.filter(pk=serializer.data['id']).first()
        models.Versions.objects.create(version=data['version'],version_type=data.get('version_type'), plugin_instructions=data['plugin_instructions'],plugin_markdown_text=data['plugin_markdown_text'],
                                       software=soft_obj)
        return Response(serializer.data)
from rest_framework_simplejwt.tokens import Token
from jwt import decode as jwt_decode
class DownLoadZipFile(GenericAPIView):
    # authentication_classes = (JWTAuthentication, )
    queryset = models.Software.objects.all()
    serializer_class = serializers.SoftwareReleaseGETModelSerializer
    def get(self, request, id,*args, **kwargs):

        token = request.query_params.get('token')
        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        print(decoded_data)
        jwt_obj = JwtAuth()
        ret = jwt_obj.check_jwt_token(token)

        print(ret)
        if ret['status'] !=200:
            raise APIException({"detail": "没有权限下载"})
        payload=ret['payload']
        user=models.UserInfo.objects.filter(pk=payload['user_id']).first()
        # id= int(self.request.query_params.get('id'))
        obj = models.Software.objects.filter(pk=id).first()
        if obj is None:
            raise APIException({"detail": "软件不存在"})
        if obj.release_form == 0:  # 免费软件
            try:
                path = str(obj.source_code_file)
                file_path = str(os.path.join(settings.MEDIA_ROOT, str(obj.source_code_file).replace('\\', '/')))
                exist_obj=models.DownloadRecord.objects.filter(softwares=obj.pk,users=user.pk).exists()
                if not exist_obj:
                    models.DownloadRecord.objects.create(softwares=obj,users=user)
                    obj.number_downloads = F('number_downloads') + 1  # 下载次数+1
                    obj.save()
                    response = FileResponse(open(str(file_path), 'rb'))
                    response['Content-Type'] = 'application/zip'
                    response['Content-Disposition'] = 'attachment; filename="%s"' % path.split('/')[-1]
                    return response
                else:
                    response = FileResponse(open(str(file_path), 'rb'))
                    response['Content-Type'] = 'application/zip'
                    response['Content-Disposition'] = 'attachment; filename="%s"' % path.split('/')[-1]
                    return response
            except Exception:
                raise Http404
        elif obj.release_form == 1:
            obj_order = Order.objects.filter(software=id,user=user,status__in=[2,5]).first()
            if obj_order is None:
                raise APIException({"detail": "没有权限下载"})
            order_status = Order.objects.filter(order_id=obj_order.order_id).first()
            if order_status:
                if order_status.status in [2,5,]:
                    try:
                        path = str(obj.source_code_file)
                        file_path = str(os.path.join(settings.MEDIA_ROOT, str(obj.source_code_file).replace('\\', '/')))
                        exist_obj = models.DownloadRecord.objects.filter(softwares=obj.pk, users=user.pk).exists()
                        if not exist_obj:
                            models.DownloadRecord.objects.create(softwares=obj, users=user)
                            obj.number_downloads = F('number_downloads') + 1  # 下载次数+1
                            obj.save()
                            response = FileResponse(open(str(file_path), 'rb'))
                            response['Content-Type'] = 'application/zip'
                            response['Content-Disposition'] = 'attachment; filename="%s"' % path.split('/')[-1]
                            return response
                        else:
                        #     wrapper = FileWrapper(open(filename, 'rb'))
                            response = FileResponse(open(str(file_path), 'rb'))
                            response['Content-Type'] = 'application/octet-stream'
                            response['Content-Disposition'] = 'attachment; filename="%s"' % urlquote(path.split('/')[-1])
                            response['Content-Length'] = os.path.getsize(file_path)
                            return response
                    except Exception:
                        raise Http404
                else:
                    raise APIException({"detail": "没有权限下载"})
            else:
                raise APIException({"detail": "没有权限下载"})
        else:
            raise APIException({"detail": "没有权限下载"})


from .serializers import CommentSoftGetModelSerializer


class CommentGetView(ViewSetMixin, ListAPIView):
    """
    GET:
        list:获取根评论下的所有子评论
    """

    serializer_class = CommentSoftGetModelSerializer
    queryset = models.Comment_soft.objects.all()

    def get_queryset(self):
        root_id = self.request.query_params.get('root')
        queryset = models.Comment_soft.objects.filter(root_id=root_id, is_delete=False)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return APIResponse(result=serializer.data)


from .serializers import CommentSoftPostModelSerializer
from django.db.models import F


class CommentCreateView(ViewSetMixin, CreateAPIView):
    """
    POST:
        create:创建评论
    """
    authentication_classes = (JWTAuthentication, )
    serializer_class = CommentSoftPostModelSerializer
    queryset = models.Comment_soft.objects.all()

    def create(self, request, *args, **kwargs):
        if request.user.pk is None:
            raise APIException({'detail': '用户未登录'})
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = models.UserInfo.objects.filter(pk=request.user.pk).first()
        serializer.save(user=user)
        softwares_id = self.request.data.get('softwares')
        models.Software.objects.filter(id=softwares_id).update(comment_count=F('comment_count') + 1)  # 每评论一次计数一次
        return APIResponse(result=serializer.data)



from django.db.models import Max
# 我发布的插件列表(未调通)
class MySoftwareReleaseGetView(ModelViewSet):
    """
    list:
        Response a data (get)
    retrieve:
        Response a data retrieve（get）
    """
    pagination_class = MyPageNumberPagination
    authentication_classes = (JWTAuthentication, )
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "people_buy", "create_time", "update_time", ]
    filter_class = SoftwareFilter
    lookup_field = 'id'
    queryset = models.Software.objects.filter().all()
    serializer_class = serializers.SoftwareReleaseGETModelSerializer

    def get_queryset(self):
        return models.Software.objects.filter(user=self.request.user,is_delete=False)

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.SoftwareReleaseGETModelSerializer
        elif self.action in ['retrieve','partial_update',]:
            return serializers.MyPublishPluginsDetailModelSerializer
        elif self.action in ['update']:
            return serializers.RedactSoftwarePutModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    # def update(self, request, *args, **kwargs):
    #     print(kwargs.get('id'))
    #     instance = self.get_object()
    #     software_obj=models.Software.objects.filter(id=kwargs.get('id')).first()
    #     release_form=request.data.get('release_form') # 获取免费0或付费1状态
    #     if release_form == 0:  # 0为免费
    #         source_code_file=request.FILES.get('source_code_file')
    #
    #         dict_data = {
    #             'affiliation': request.data.get('affiliation'),
    #             'currency': request.data.get('currency'),
    #             'name': request.data.get('name'),
    #             'brief': request.data.get('brief'),
    #             'source_code_file': source_code_file,
    #             'direction_for_use': request.data.get('direction_for_use'),
    #             'rnb': 0,
    #             'dollar': 0,
    #             'release_form': int(request.data.get('release_form')),
    #         }
    #
    #         serializer = self.get_serializer(instance, data=dict_data, context={'request': request})
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_update(serializer)
    #         result = models.Versions.objects.filter(software=software_obj).last()
    #         models.Versions.objects.filter(id=result.id).update(version=request.data.get('version'),plugin_instructions=request.data.get('plugin_instructions'),)
    #         tab_name = request.data.get('tab_name')
    #         if '，' in tab_name:
    #             tab_list = tab_name.split('，')  # 中文逗号
    #             for item in tab_list:
    #                 models.Tab.objects.filter(software=software_obj).update(tab_name=item)
    #             return Response(serializer.data)
    #         elif ',' in tab_name:
    #             tab_list = tab_name.split(',')  # 英文逗号
    #             for item in tab_list:
    #                 models.Tab.objects.filter(software=software_obj).update(tab_name=item)
    #             return Response(serializer.data)
    def update(self, request, *args, **kwargs):
        print(kwargs.get('id'))
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data=self.request.data
        print(data)


        release_form=data.get('release_form')
        if int(release_form) == 0: # 修改为免费插件
            source_code_file = self.request.FILES.get('source_code_file')
            if source_code_file:
                if source_code_file:
                    if source_code_file.size > 209715200:  # 104857600->100M
                        raise APIException({"detail": "文件大小不大于200M"})
                    file_type = source_code_file.name.split('.')[1]
                    if file_type not in ['zip']:
                        raise APIException({"detail": "文件类型必须是zip"})
                    print(source_code_file.size)

                    dict_data = {
                        'affiliation':data.get('affiliation',instance.affiliation),
                        'currency':None,
                        'name':data.get('name',instance.name),
                        'brief':data.get('brief',instance.brief),
                        'source_code_file':self.request.FILES.get('source_code_file'),
                        'direction_for_use':data.get('direction_for_use',instance.direction_for_use),
                        'rnb':float(0.00),
                        'dollar':float(0.00),
                        'release_form': int(data.get('release_form')),
                        'direction_markdown_text':data.get('direction_markdown_text'),
                        'check':0,
                        'putaway':False,
                    }
            else:
                dict_data = {
                    'affiliation': data.get('affiliation', instance.affiliation),
                    'currency': None,
                    'name': data.get('name', instance.name),
                    'brief': data.get('brief', instance.brief),
                    'source_code_file': instance.source_code_file,
                    'direction_for_use': data.get('direction_for_use', instance.direction_for_use),
                    'rnb': float(0.00),
                    'dollar': float(0.00),
                    'release_form': int(data.get('release_form')),
                    'direction_markdown_text':data.get('direction_markdown_text'),
                    'check': 0,
                    'putaway': False,
                }
            serializer = self.get_serializer(instance, data=dict_data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            soft_obj = models.Software.objects.filter(pk=instance.pk).first()
            result=models.Versions.objects.filter(software=soft_obj).values('id').annotate(max_id=Max('id'))
            result_id_list = [item['max_id'] for item in result]
            models.Versions.objects.filter(id__in=result_id_list).update(version=data.get('version'),plugin_instructions=data.get('plugin_instructions'),version_type=data.get('version_type'))
            models.Tab.objects.filter(software=soft_obj).delete()
            tab_name = data.get('tab_name')
            if '，' in tab_name:
                tab_list = tab_name.split('，')  # 中文逗号
                for item in tab_list:
                    models.Tab.objects.create(software=soft_obj,tab_name=item)
                return Response(serializer.data)
            elif ',' in tab_name:
                tab_list = tab_name.split(',')  # 英文逗号
                for item in tab_list:
                    models.Tab.objects.create(software=soft_obj,tab_name=item)
                return Response(serializer.data)
            else:  # 没逗号
                models.Tab.objects.create(software=soft_obj,tab_name=tab_name)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        elif int(release_form) == 1: # 付费
            currency = int(data.get('currency',instance.currency)) # 币种
            if currency == 0: # 发布人民币插件
                source_code_file = self.request.FILES.get('source_code_file')
                if source_code_file:
                    if source_code_file.size > 209715200:  # 104857600->100M
                        raise APIException({"detail": "文件大小不大于200M"})
                    if source_code_file:
                        file_type = source_code_file.name.split('.')[1]
                        if file_type not in ['zip']:
                            raise APIException({"detail": "文件类型必须是zip"})
                        dict_data = {
                            'affiliation': data.get('affiliation', instance.affiliation),
                            'currency': data.get('currency', instance.currency),
                            'name': data.get('name', instance.name),
                            'brief': data.get('brief', instance.brief),
                            'source_code_file': data.get('source_code_file',instance.source_code_file),
                            'direction_for_use': data.get('direction_for_use', instance.direction_for_use),
                            'rnb': float(data.get('rnb')),
                            'dollar': 0,
                            'release_form': int(data.get('release_form')),
                            'direction_markdown_text':data.get('direction_markdown_text'),
                            'check':0,
                            'putaway':False,
                        }
                else:
                    dict_data = {
                        'affiliation': data.get('affiliation', instance.affiliation),
                        'currency': data.get('currency', instance.currency),
                        'name': data.get('name', instance.name),
                        'brief': data.get('brief', instance.brief),
                        'source_code_file':instance.source_code_file,
                        'direction_for_use': data.get('direction_for_use', instance.direction_for_use),
                        'rnb': float(data.get('rnb')),
                        'dollar': 0,
                        'release_form': int(data.get('release_form')),
                        'direction_markdown_text':data.get('direction_markdown_text'),
                        'check': 0,
                        'putaway': False,
                    }

                serializer = self.get_serializer(instance, data=dict_data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                soft_obj = models.Software.objects.filter(pk=instance.pk).first()
                result = models.Versions.objects.filter(software=soft_obj).values('id').annotate(max_id=Max('id'))
                result_id_list = [item['max_id'] for item in result]
                models.Versions.objects.filter(id__in=result_id_list).update(version=data.get('version'),plugin_instructions=data.get('plugin_instructions'),version_type=data.get('version_type'))
                models.Tab.objects.filter(software=soft_obj).delete()
                tab_name = data.get('tab_name')
                if '，' in tab_name:
                    tab_list = tab_name.split('，')  # 中文逗号
                    for item in tab_list:
                        models.Tab.objects.create(software=soft_obj, tab_name=item)
                    return Response(serializer.data)
                elif ',' in tab_name:
                    tab_list = tab_name.split(',')  # 英文逗号
                    for item in tab_list:
                        models.Tab.objects.create(software=soft_obj, tab_name=item)
                    return Response(serializer.data)
                else:  # 没逗号
                    models.Tab.objects.create(software=soft_obj, tab_name=tab_name)
                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}

                return Response(serializer.data)
            else: # 发布的美元插件
                source_code_file = self.request.FILES.get('source_code_file')
                if source_code_file:
                    if source_code_file:
                        if source_code_file.size > 209715200:  # 104857600->100M
                            raise APIException({"detail": "文件大小不大于200M"})
                        file_type = source_code_file.name.split('.')[1]
                        if file_type not in ['zip']:
                            raise APIException({"detail": "文件类型必须是zip"})
                        instance.source_code_file.delete()
                        dict_data = {
                            'affiliation': data.get('affiliation', instance.affiliation),
                            'currency': data.get('currency', instance.currency),
                            'name': data.get('name', instance.name),
                            'brief': data.get('brief', instance.brief),
                            'source_code_file': data.get('source_code_file', instance.source_code_file),
                            'direction_for_use': data.get('direction_for_use', instance.direction_for_use),
                            'rnb': 0,
                            'dollar': data.get('dollar'),
                            'release_form': int(data.get('release_form')),
                            'direction_markdown_text':data.get('direction_markdown_text'),
                            'check':0,
                            'putaway':False,
                        }
                else:
                    dict_data = {
                        'affiliation': data.get('affiliation', instance.affiliation),
                        'currency': data.get('currency', instance.currency),
                        'name': data.get('name', instance.name),
                        'brief': data.get('brief', instance.brief),
                        'source_code_file': instance.source_code_file,
                        'direction_for_use': data.get('direction_for_use', instance.direction_for_use),
                        'rnb': 0,
                        'dollar': data.get('dollar'),
                        'release_form': int(data.get('release_form')),
                        'direction_markdown_text':data.get('direction_markdown_text'),
                        'check': 0,
                        'putaway': False,
                    }

                serializer = self.get_serializer(instance, data=dict_data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                soft_obj = models.Software.objects.filter(pk=instance.pk).first()
                result = models.Versions.objects.filter(software=soft_obj).values('id').annotate(max_id=Max('id'))
                result_id_list = [item['max_id'] for item in result]
                models.Versions.objects.filter(id__in=result_id_list).update(version=data.get('version'),plugin_instructions=data.get('plugin_instructions'),version_type=data.get('version_type'),plugin_markdown_text=data.get('plugin_markdown_text'))
                models.Tab.objects.filter(software=soft_obj).delete()
                tab_name = data.get('tab_name')
                if '，' in tab_name:
                    tab_list = tab_name.split('，')  # 中文逗号
                    for item in tab_list:
                        models.Tab.objects.create(software=soft_obj, tab_name=item)
                    return Response(serializer.data)
                elif ',' in tab_name:
                    tab_list = tab_name.split(',')  # 英文逗号
                    for item in tab_list:
                        models.Tab.objects.create(software=soft_obj, tab_name=item)
                    return Response(serializer.data)
                else:  # 没逗号
                    models.Tab.objects.create(software=soft_obj, tab_name=tab_name)
                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}

                return Response(serializer.data)
        else:
            raise APIException({'detail':'出错'})
    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)



class RedactSoftware(ModelViewSet):
    pagination_class = MyPageNumberPagination
    authentication_classes = (JWTAuthentication, )
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "people_buy", "create_time", "update_time", ]
    filter_class = SoftwareFilter
    lookup_field = 'id'
    queryset = models.Software.objects.filter().all()
    serializer_class = serializers.RedactSoftwarePutModelSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)



class Bannerlistview(ModelViewSet):
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('orders')[
               :settings.BANNER_COUNT]
    serializer_class = serializers.BannerGETModelSerializer

    def get_queryset(self):
        queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('orders')[
                   :settings.BANNER_COUNT]
        return queryset

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.BannerGETModelSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

