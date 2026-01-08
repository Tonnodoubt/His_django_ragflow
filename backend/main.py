from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from services import HistoryQuestionService
import uvicorn

# 1. 定义请求的数据结构
class QuestionRequest(BaseModel):
    topic: str
    difficulty: str = "普通"

# 2. 初始化 App 和 服务
app = FastAPI(title="历史出题 Agent API")

# 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 构建专家 Prompt
def build_expert_prompt(topic, difficulty):
    # 核心素养定义 (基于课标)
    competencies = """
    1. 唯物史观：揭示人类社会历史客观基础及发展规律。
    2. 时空观念：在特定的时间联系和空间联系中对事物进行观察、分析。
    3. 史料实证：对获取的史料进行辨析，并运用史料努力重现历史真实。
    4. 历史解释：以史料为依据，客观地认识和评判历史。
    5. 家国情怀：学习和探究历史应具有的人文追求与国家认同。
    """

    prompt = f"""
    # Role
    你是一位资深的高中历史教师和命题专家，精通《普通高中历史课程标准（2017年版2025年修订）》。

    # Task
    请基于知识库中的“课程标准”内容，围绕主题【{topic}】，设计一道【{difficulty}】难度的单项选择题。

    # Constraints & Guidelines (必须严格遵守)
    1. **课标对标**：首先在知识库中检索该主题对应的“内容要求”和“学业质量标准”。
    2. **史料情境**：题目**必须**包含一段“史料材料”（如古籍引文、名人名言），不能是纯粹的知识记忆题。
    3. **核心素养**：题目解析中必须明确指出了考查了哪种核心素养。
    4. **干扰项设计**：错误选项必须具有干扰性，符合高中生认知水平。

    # Output Format (JSON Only)
    请仅返回合法的 JSON 格式，不要包含 Markdown 标记。
    **注意：字段名必须严格如下：**
    {{
        "question_text": "（这里写基于史料的完整题干，例如：‘据《...》记载...，这反映了？’）",
        "options": ["A. 选项内容", "B. 选项内容", "C. 选项内容", "D. 选项内容"],
        "correct_answer": "（只写选项内容，如 'A. 选项内容'，需与options中一致）",
        "explanation": "【课标依据】本题对应课标专题... \\n【素养考查】本题考查了...素养。\\n【解析】正选...；A错在...；B错在..."
    }}
    """
    return prompt

service = HistoryQuestionService()

# 4. 定义接口路由
@app.post("/api/generate-quiz")
async def generate_quiz(request: QuestionRequest):
    """
    接收前端发来的 topic，构建专家 Prompt，调用 RAGFlow 生成题目
    """
    print(f"📡 API 收到请求: {request.topic}")
    
    # 1. 生成专家 Prompt
    expert_prompt = build_expert_prompt(request.topic, request.difficulty)
    
    # 2. 传递 Prompt 给 Service
    result = service.generate_question(request.topic, request.difficulty, custom_prompt=expert_prompt)
    
    if not result:
        raise HTTPException(status_code=500, detail="生成失败，RAGFlow 无响应或解析错误")
        
    return {
        "status": "success",
        "data": result
    }

# 5. 启动服务
if __name__ == "__main__":
    print("🚀 后端服务启动中: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)