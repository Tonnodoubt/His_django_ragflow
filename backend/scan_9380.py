import requests
import os
import dotenv
from pathlib import Path

# 1. 加载 Key
current_dir = Path(__file__).resolve().parent
env_path = current_dir.parent / '.env'
dotenv.load_dotenv(dotenv_path=env_path)
API_KEY = os.getenv("RAGFLOW_API_KEY")
CHAT_ID = os.getenv("RAGFLOW_CHAT_ID")

# 2. 目标：直连后端 9380
BASE_URL = "http://localhost:9380"
print(f"📡 开始扫描后端: {BASE_URL}")

# 3. 定义所有可能的路径组合
# RAGFlow 不同版本变动很大，我们把可能的全试一遍
candidates = [
    # 根目录尝试
    "/", 
    "/api",
    "/v1",
    
    # OpenAI 兼容接口可能的位置
    "/chat/completions",
    "/v1/chat/completions",
    "/api/v1/chat/completions",
    "/ragflow/chat/completions",
    "/ragflow/api/v1/chat/completions",
    
    # 原生接口可能的位置 (Native)
    "/conversation/completion",
    "/api/conversation/completion",
    "/api/v1/conversation/completion",
    "/v1/conversation/completion",
    
    # 辅助接口 (用来测试连通性)
    "/api/v1/dialog/list",
    "/v1/dialog/list",
    "/docs",      # Swagger UI
    "/openapi.json" # API 定义文件
]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 这是一个最小的 Payload，两边都能吃
payload = {
    "conversation_id": "new", 
    "model": CHAT_ID,
    "messages": [{"role": "user", "content": "ping"}],
    "dialog_id": CHAT_ID
}

found_any = False

for path in candidates:
    url = f"{BASE_URL}{path}"
    print(f"Trying: {path:<35}", end="")
    
    try:
        # 统一用 POST 测试 (除了 docs 用 GET)
        if "docs" in path or "json" in path or path == "/" or path == "/api":
            resp = requests.get(url, timeout=3)
        else:
            resp = requests.post(url, json=payload, headers=headers, timeout=3)
            
        status = resp.status_code
        
        if status == 404:
            print("❌ 404 (无)")
        elif status == 405:
            print("⚠️ 405 (路径存在! 方法不对)")
            print(f"    >> 🎉 发现端点: {url} (请尝试改用 GET 或 POST)")
            found_any = True
        elif status == 401:
            print("🔒 401 (路径存在! 需要认证)")
            # 401 说明路径是对的，只是 Key 没被接受，或者这是 Cookie 接口
            print(f"    >> 💡 线索: {url} 是一个有效接口！")
            found_any = True
        elif status == 200:
            print("✅ 200 (通了!)")
            print(f"    >> 🏆 最终答案: {url}")
            found_any = True
            break # 找到了就停
        else:
            print(f"❓ {status} (有响应)")
            print(f"    >> 💡 线索: {url}")
            found_any = True
            
    except Exception as e:
        print(f"💥 连接错: {e}")

print("\n------------------------------------------------")
if not found_any:
    print("😱 扫描结束，9380 端口似乎拒绝了所有已知路径。")
    print("建议：在浏览器打开 http://localhost:9380/docs 看看有没有 Swagger 文档？")
else:
    print("🚀 请根据上面标记为 '💡' 或 '🏆' 的路径修改您的 .env")