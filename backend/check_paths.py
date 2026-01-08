import os
import requests
import dotenv
from pathlib import Path

# 1. 加载配置
current_dir = Path(__file__).resolve().parent
env_path = current_dir.parent / '.env'
dotenv.load_dotenv(dotenv_path=env_path)

api_key = os.getenv("RAGFLOW_API_KEY")
# 注意：这里我们只取主机部分，比如 http://localhost
# 无论 .env 里怎么写，我们强制拆分出来基础域名，方便拼接测试
raw_base = os.getenv("RAGFLOW_API_BASE", "http://localhost/api/v1")
if "/api" in raw_base:
    host_only = raw_base.split("/api")[0] # 拿到 http://localhost
else:
    host_only = raw_base.rstrip("/")

print(f"🔎 正在探测 RAGFlow 主机: {host_only}")
print(f"🔑 使用 Key: {api_key[:10]}...")

headers = {"Authorization": f"Bearer {api_key}"}

# 2. 定义我们要测试的路径列表
# 这些是不同版本 RAGFlow 可能存在的入口
paths_to_test = [
    # [GET] 测试是否通畅的最简单接口：获取对话列表
    ("GET",  "/api/v1/dialog/list"),       # 标准路径
    ("GET",  "/api/dialog/list"),          # 无版本号
    ("GET",  "/v1/api/dialog/list"),       # 某些怪异配置
    
    # [POST] 原生对话接口
    ("POST", "/api/v1/conversation/completion"), 
    
    # [POST] OpenAI 兼容接口
    ("POST", "/api/v1/chat/completions"),
]

print("\n🚀 开始路径探测...\n")

success_found = False

for method, path in paths_to_test:
    full_url = f"{host_only}{path}"
    print(f"Testing: {method} {full_url} ...", end=" ")
    
    try:
        if method == "GET":
            resp = requests.get(full_url, headers=headers, timeout=5)
        else:
            # POST 请求随便发点空的，只要不报 404 就算找到路了
            resp = requests.post(full_url, headers=headers, json={}, timeout=5)
        
        if resp.status_code == 404:
            print("❌ 404 (不存在)")
        elif resp.status_code == 401:
            print("⚠️ 401 (路径存在但Key不对) -> 说明路径是对的！")
            success_found = True
        elif resp.status_code == 200:
            print("✅ 200 (完美连接!)")
            success_found = True
            if method == "GET":
                print("   >> 返回数据片段:", str(resp.json())[:100])
        elif resp.status_code == 405:
            print("⚠️ 405 (方法不允许) -> 说明路径存在！")
            success_found = True
        else:
            print(f"❓ {resp.status_code} (其他错误，但至少不是404)")
            print("   >>", resp.text[:100])
            success_found = True
            
    except Exception as e:
        print(f"💥 连接异常: {e}")

print("\n------------------------------------------------")
if not success_found:
    print("😓 所有常用路径都测试失败。")
    print("可能原因：Nginx 配置修改了 /api 前缀，或者 Docker 端口映射不是 80。")
else:
    print("🎉 只要上面有一个不是 404，就说明我们找到路了！请使用那个路径。")