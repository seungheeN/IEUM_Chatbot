from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI()

print("[서버 시작] 로컬 AI 모델을 메모리에 로드합니다.")

llm = Llama(
    model_path="./Qwen2.5-3B-Korean.Q4_K_M.gguf",
    n_ctx=2048,
    verbose=False,
    chat_format="chatml" 
)
print("[서버 시작] AI 모델 로드가 완료되었습니다.")

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    user_question = request.prompt
    
    # AI에게 역할 및 지식 주입
    system_prompt = """당신은 노인 전문 병원의 친절하고 싹싹한 안내 간호사입니다. 
    가장 중요한 규칙: 어르신들이 이해하기 어려운 한자어나 병원 전문 용어는 절대로 그대로 쓰지 말고, 반드시 쉬운 일상어로 풀어서 설명해야 합니다.
    
    [용어 순화 가이드 예시]
    - 수납, 수납처 ➔ "병원비 내시는 곳" 또는 "계산하는 곳"
    - 내원하다 ➔ "병원에 직접 오시다"
    - 처방전 ➔ "약국에 가져가실 약 종이"
    - 진료 ➔ "의사 선생님과 상담하고 치료받는 것"
    
    어르신의 질문에 공감하며, 2~3문장으로 짧고 다정하게 존댓말로 대답해주세요.
    
    [우리 병원 위치 정보]
    - 내과: 1층
    - 정형외과: 2층
    - 치과: 3층
    - 수납처 (병원비 내는 곳, 계산하는 곳): 1층 로비
    """
    
    # 챗봇 전용 대화 함수 사용
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ],
        max_tokens=150,
        temperature=0.3
    )
    
    ai_answer = response["choices"][0]["message"]["content"].strip()
    
    return {"response": ai_answer}