from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llama_cpp import Llama
from typing import List, Dict

# [RAG 모듈]
from rag.retriever import get_rag_context, get_terms_context, simplify_terms

app = FastAPI()

# ===============================
# [CORS 설정]
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 주소의 접근 허용 (테스트 단계)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST 등 모든 전송 방식 허용
    allow_headers=["*"],  # 모든 헤더 정보 허용
)

print("[서버 시작] 로컬 AI 모델을 메모리에 로드합니다.")
llm = Llama(
    model_path="./qwen2.5-3b-instruct.Q4_K_M.gguf",
    n_ctx=2048,
    verbose=False,
    chat_format="chatml"
)
print("[서버 시작] AI 모델 로드가 완료되었습니다.")

# 메모리 로직
session_memories: Dict[str, List[Dict[str, str]]] = {}

# 프론트엔드 데이터 규격 정의
class ChatRequest(BaseModel):
    session_id: str  # 대화방 구별용 고유 ID (Ex: "user_123")
    prompt: str      # 질문 문장

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    sid = request.session_id
    user_question = request.prompt

    rag_context = get_rag_context(user_question, top_k=3)
    terms_context = get_terms_context(limit=30)
    easy_question = simplify_terms(user_question) # 프롬프트 최적화용 보조 단어

    rag_prompt = f"""[병원 안내 관련 문서 정보]
    {rag_context}

    [어르신 맞춤용 어려운 용어 해설 사전]
    {terms_context}

    [어르신의 실제 질문]
    {user_question} (참고 키워드: {easy_question})

    [지시사항]
    주어진 '병원 안내 관련 문서 정보'와 '어려운 용어 해설 사전'의 내용에만 절대적으로 기반하여 어르신의 질문에 답변하세요. 
    문서에 나오지 않는 내용은 상상해서 지어내거나 거짓말하지 말고, 모르는 내용이라면 "확인 후 안내해 드리겠다"고 답변하세요."""
    
    # 처음 대화를 시작하는 방이라면 기본 페르소나 주입
    if sid not in session_memories:
        session_memories[sid] = [
            {"role": "system", "content": "당신은 노인 전문 병원의 친절하고 싹싹한 안내 간호사입니다. 어르신의 질문에 깊이 공감하며, 2~3문장으로 짧고 다정하게 존댓말로 대답해주세요."}
        ]
    
    # 신규 질문을 해당 방 기록에 누적
    session_memories[sid].append({"role": "user", "content": rag_prompt})

    # 과거 대화 흐름을 고려해 AI 추론 실행
    response = llm.create_chat_completion(
        messages=session_memories[sid],
        max_tokens=150,
        temperature=0.3
    )
    
    ai_answer = response["choices"][0]["message"]["content"].strip()
    
    # AI의 대답을 기록에 누적
    session_memories[sid].append({"role": "assistant", "content": ai_answer})
    
    # 대화가 길어지면 앞부분을 잘라내어 과부하 방지
    if len(session_memories[sid]) > 11:
        session_memories[sid] = [session_memories[sid][0]] + session_memories[sid][3:]
        
    # 프론트엔드에게 최종 답변 반환
    return {"response": ai_answer}