import os
import json
import re
import httpx
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

class HistoryQuestionService:
    def __init__(self):
        self.base_url = os.getenv("RAGFLOW_BASE_URL")
        self.chat_id = os.getenv("RAGFLOW_CHAT_ID")
        self.api_key = os.getenv("RAGFLOW_API_KEY")
        
        if not self.base_url or not self.chat_id or not self.api_key:
            raise ValueError("❌ 错误: 环境变量未完整设置，请检查 .env 文件！")

        self.full_url = f"{self.base_url}/chats_openai/{self.chat_id}"
        
        # 忽略系统代理，防止 VPN 干扰
        custom_http_client = httpx.Client(trust_env=False)

        self.client = OpenAI(
            base_url=self.full_url,
            api_key=self.api_key,
            http_client=custom_http_client
        )

    def _clean_json_string(self, text: str) -> str:
        # 移除 Markdown 代码块
        pattern = r"```json\s*(.*?)\s*```"
        match = re.search(pattern, text, re.DOTALL)
        if match: return match.group(1)
        
        # 寻找首尾括号
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1: return text[start : end + 1]
        return text

    # 👇 修改了这里：增加 custom_prompt 参数
    def generate_question(self, topic: str, difficulty: str = "普通", custom_prompt: str = None):
        print(f"🤖 [Service] 收到请求: 生成关于 '{topic}' 的 {difficulty} 题")
        
        # 如果传入了自定义 Prompt，就用传入的；否则用默认的
        if custom_prompt:
            final_prompt = custom_prompt
        else:
            final_prompt = f"""
            请生成一道关于【{topic}】的【{difficulty}】难度历史选择题。
            要求：必须基于知识库，返回标准 JSON，包含 question_text, options, correct_answer, explanation。
            """

        try:
            response = self.client.chat.completions.create(
                model="default",
                messages=[{"role": "user", "content": final_prompt}],
                stream=False
            )
            
            raw_content = response.choices[0].message.content
            # 打印一下原始返回，方便调试
            print(f"📝 RAGFlow 返回原始内容: {raw_content[:100]}...")
            
            cleaned_json = self._clean_json_string(raw_content)
            return json.loads(cleaned_json)

        except Exception as e:
            print(f"❌ [Service] 生成失败: {e}")
            return None