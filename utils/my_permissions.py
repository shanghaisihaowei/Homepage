from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    message = '不是超级用户，或没有认证成为开发者不能访问'
    def has_permission(self, request, view):
        user_type = request.user.user_type
        print(user_type)
        if user_type == 1: # 开发者
            return True
        elif request.user.is_superuser == 1: # 超级用户
            return True
        else: # 普通用户
            return False