from django.apps import AppConfig


class MyWalletConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_wallet'
    verbose_name = "用户钱包管理"