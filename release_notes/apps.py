from django.apps import AppConfig


class ReleaseNotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'release_notes'
    verbose_name = "发行版本管理"