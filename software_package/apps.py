from django.apps import AppConfig


class SoftwarePackageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'software_package'
    verbose_name = "插件管理"