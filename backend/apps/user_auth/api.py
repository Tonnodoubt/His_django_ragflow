from ninja import Router
from pydantic import BaseModel, EmailStr
from django.contrib.auth import authenticate
from .jwt import create_token

router = Router()

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

@router.post("/login", auth=None) # 公开接口
def login(request, payload: LoginSchema):
    user = authenticate(email=payload.email, password=payload.password)
    if not user:
        return 401, {"message": "账号或密码错误"}
    
    # 检查邮箱验证状态
    # if not user.is_email_verified:
    #     return 403, {"message": "请先验证邮箱"} 

    token = create_token(user.id)
    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }