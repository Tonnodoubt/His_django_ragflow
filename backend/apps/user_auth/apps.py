from django.apps import AppConfig

class UserAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 关键修改：必须写全路径
    name = 'backend.apps.user_auth'
    label = 'user_auth'
