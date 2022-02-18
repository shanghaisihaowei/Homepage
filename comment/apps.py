from django.apps import AppConfig


class CommentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comment'
    verbose_name = "用户文章评论管理"