from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 关键修改：必须写全路径，不能只写 'users'
    name = 'backend.apps.users' 
    # 显式指定 label，方便 AUTH_USER_MODEL 调用
    label = 'users'