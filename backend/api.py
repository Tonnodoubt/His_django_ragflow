from ninja import NinjaAPI
from backend.apps.user_auth.api import router as auth_router

api = NinjaAPI(title="History Agent API", version="1.0.0")

# 挂载鉴权路由
api.add_router("/auth", auth_router)