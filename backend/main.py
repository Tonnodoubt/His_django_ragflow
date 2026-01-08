from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services import HistoryQuestionService
import uvicorn

# 1. 定义请求的数据结构
class QuestionRequest(BaseModel):
    topic: str
    difficulty: str = "普通"

# 2. 初始化 App 和 服务
app = FastAPI(title="历史出题 Agent API")
service = HistoryQuestionService()

# 3. 定义接口路由
@app.post("/api/generate-quiz")
async def generate_quiz(request: QuestionRequest):
    """
    接收前端发来的 topic，调用 RAGFlow 生成题目
    """
    print(f"📡 API 收到请求: {request.topic}")
    
    result = service.generate_question(request.topic, request.difficulty)
    
    if not result:
        raise HTTPException(status_code=500, detail="生成失败，RAGFlow 无响应或解析错误")
        
    return {
        "status": "success",
        "data": result
    }

# 4. 启动服务 (仅在直接运行此文件时触发)
if __name__ == "__main__":
    print("🚀 后端服务启动中: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)