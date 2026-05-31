import os
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# .env 파일에서 키 값 받아 구글에 로그인
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini 모델 선택
model = genai.GenerativeModel('gemini-3.5-flash')

app = FastAPI()

class ChatRequest(BaseModel):
    user_message: str

# ==========================================
# True: 작동 테스트 모드 / False: 실제 API 통신 모드
# ==========================================
USE_MOCK = True

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    try:
        user_input = request.user_message
        
        # 작동 및 프론트엔드 연동 테스트용
        if USE_MOCK:
            return {
                "status": "success",
                "bot_reply": f"[테스트용 더미 답변] '{user_input}'라고 말씀하셨군요? 1층 창구로 가시면 됩니다."
            }
            
        # 실제 API 통신 모드
        else:
            prompt = f"너는 친절한 시니어 병원 안내 챗봇이야. 다음 질문에 어르신 말투로 짧게 대답해: {user_input}"
            response = model.generate_content(prompt)
            
            return {
                "status": "success",
                "bot_reply": response.text
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"죄송해요, 잠시 후 다시 말씀해 주시겠어요? (에러: {str(e)})"
        }