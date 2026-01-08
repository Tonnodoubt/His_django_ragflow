from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    自定义用户模型
    对应文档: docs/backend/modules-design/user.md
    """
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', '管理员'
        AGENT = 'AGENT', 'Agent工具人'
        CLIENT = 'CLIENT', '甲方/客户' # V1规划

    # 覆盖默认字段，使用 email 作为唯一标识
    email = models.EmailField("邮箱地址", unique=True)
    username = models.CharField("用户名", max_length=150, blank=True)
    
    role = models.CharField("角色", max_length=10, choices=Role.choices, default=Role.CLIENT)
    phone = models.CharField("手机号", max_length=20, blank=True, null=True, unique=True)
    avatar = models.ImageField("头像", upload_to="avatars/", null=True, blank=True)
    is_email_verified = models.BooleanField("邮箱已验证", default=False) #

    # 将 email 设为登录账号字段
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class ClientProfile(models.Model):
    """
    甲方档案 (V1)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    company_name = models.CharField("公司名称", max_length=100)
    industry = models.CharField("行业", max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.company_name} ({self.user.email})"