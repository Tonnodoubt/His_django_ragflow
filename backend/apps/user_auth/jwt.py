import jwt
import time
from django.conf import settings
from ninja.security import HttpBearer
from django.contrib.auth import get_user_model

# 获取当前激活的用户模型（即 users.User）
User = get_user_model()

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            # 使用 Django 的 SECRET_KEY 解密
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            
            # 检查是否过期
            if payload.get("exp") < time.time():
                return None
                
            if user_id:
                try:
                    return User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return None
        except Exception:
            # 任何解码错误或异常都视为认证失败
            return None

def create_token(user_id: int):
    """
    签发 Token 工具函数
    """
    payload = {
        "user_id": user_id,
        # Token 有效期设为 7 天
        "exp": time.time() + 60 * 60 * 24 * 7, 
        "iat": time.time()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")