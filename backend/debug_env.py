from dotenv import dotenv_values, load_dotenv
from pathlib import Path
import os

# 1. 确定路径
env_path = Path(__file__).parent / ".env"
print(f"📂 目标文件路径: {env_path}")

# 2. 检查文件是否存在
if not env_path.exists():
    print("❌ 致命错误：文件根本不存在！请检查文件名是否是 .env (而不是 .env.txt)")
    exit()

# 3. 读取文件原始内容（检查是否有乱码/BOM）
try:
    with open(env_path, "r", encoding="utf-8") as f:
        content = f.read()
        print("\n📄 [文件原始内容预览]:")
        print("-" * 20)
        print(content)
        print("-" * 20)
except Exception as e:
    print(f"❌ 读取文件失败: {e}")

# 4. 使用 dotenv 解析
config = dotenv_values(env_path)
print(f"\n🔑 [解析到的变量列表]: {list(config.keys())}")

# 5. 专门检查目标变量
target = "RAGFLOW_BASE_URL"
if target in config:
    print(f"✅ 变量 '{target}' 存在，值为: '{config[target]}'")
else:
    print(f"❌ 变量 '{target}' 未找到！")
    print("💡 可能原因：拼写错误、等号周围有空格、或者文件编码包含 BOM 头。")