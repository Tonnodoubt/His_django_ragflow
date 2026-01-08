import requests
import json

# ================= 配置区 =================
# 1. 替换为你的 RAGFlow 地址
BASE_URL = "http://127.0.0.1:9380"
# 2. 替换为你在步骤 1 获取的 ID (32位 UUID)
CHAT_ID = "d595c5a0eaa111f0823e5aa3820c5bf3"
# 3. 替换为你在步骤 2 获取的 API Key
API_KEY = "ragflow-a5_1Om3WslSn4bTEZC_rTV1lAqrOpmZFGIj841dzQZg"
# ==========================================

# 新版标准 API 路径
url = f"{BASE_URL}/api/v1/chats_openai/{CHAT_ID}/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

data = {
    "model": "你配置的模型名称", # 这一项 RAGFlow 通常会自动处理，填个默认的即可
    "messages": [
        {"role": "user", "content": "你好，请做个自我介绍。"}
    ],
    "stream": False # 如果你想测试流式输出，设为 True
}

print(f"🚀 发送请求到: {url}")
try:
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("✅ 成功连接！返回内容：")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"📡 状态码: {response.status_code}")
        print("📋 错误详情:", response.text)

except Exception as e:
    print(f"❌ 请求异常: {e}")