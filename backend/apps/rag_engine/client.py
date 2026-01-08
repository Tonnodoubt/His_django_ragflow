import httpx
import os
from django.conf import settings

class RAGFlowClient:
    def __init__(self):
        # 优先从 settings 读取，fallback 到环境变量
        self.base_url = os.getenv("RAGFLOW_API_BASE", "http://127.0.0.1:9380/v1/api")
        self.api_key = os.getenv("RAGFLOW_API_KEY")
        
        if not self.api_key:
            raise ValueError("RAGFLOW_API_KEY not found in environment variables")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _handle_response(self, response: httpx.Response):
        """统一处理 RAGFlow 的响应格式"""
        if response.status_code >= 400:
            raise Exception(f"RAGFlow API Error ({response.status_code}): {response.text}")
        
        data = response.json()
        # RAGFlow API 通常返回 { "code": 0, "data": ... }
        if data.get("code", -1) != 0:
            raise Exception(f"RAGFlow Logic Error: {data.get('message')}")
            
        return data.get("data")

    def create_dataset(self, name: str, avatar: str = ""):
        """创建知识库 (Dataset)"""
        url = f"{self.base_url}/dataset/create"
        payload = {
            "name": name,
            "avatar": avatar,
            "description": "Created by History Agent Backend",
            "permission": "me",  # 私有
            "parser_id": "naive", # 默认解析方法
            "language": "English" # 或 Chinese
        }
        
        with httpx.Client(timeout=10) as client:
            resp = client.post(url, json=payload, headers=self.headers)
            return self._handle_response(resp)

    def list_datasets(self, page=1, page_size=20):
        """获取知识库列表"""
        url = f"{self.base_url}/dataset/list"
        params = {"page": page, "page_size": page_size}
        
        with httpx.Client(timeout=10) as client:
            resp = client.get(url, params=params, headers=self.headers)
            return self._handle_response(resp)

    # 后续会添加 upload_file, retrieve 等方法