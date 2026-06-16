"""
백엔드 담당자가 import해서 사용할 파일입니다.
주요 함수:
- retrieve(query) -> str
- retrieve_top_k(query) -> list[dict]
- get_rag_context(query) -> str
- retrieve_debug(query) -> dict
- get_terms_context() -> str
- simplify_terms(text) -> str
"""

import os
import pickle
import numpy as np
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_DIR = os.path.join(BASE_DIR, "store")
DATA_DIR = os.path.join(BASE_DIR, "data")

INDEX_PATH = os.path.join(STORE_DIR, "vector_store.index")
ANSWERS_PATH = os.path.join(STORE_DIR, "answers.pkl")
TERMS_PATH = os.path.join(DATA_DIR, "terms_dataset.csv")
METADATA_PATH = os.path.join(STORE_DIR, "metadata.pkl")

MODEL_NAME = "snunlp/KR-SBERT-V40K-klueNLI-augSTS"

DEFAULT_THRESHOLD = 0.2
DEFAULT_TOP_K = 3
FALLBACK_ANSWER = (
    "죄송합니다. 해당 질문에 대한 정확한 답변을 찾지 못했습니다. "
    "병원 접수 창구나 안내 데스크에 문의해 주세요."
)

# 모듈 로드 시 1회만 초기화
print("[retriever] 모델 및 인덱스 로드 중...")
_model = SentenceTransformer(MODEL_NAME)

_index = faiss.read_index(INDEX_PATH)

with open(ANSWERS_PATH, "rb") as f:
    _answers = pickle.load(f)

if os.path.exists(METADATA_PATH):
    with open(METADATA_PATH, "rb") as f:
        _metadata = pickle.load(f)
else:
    _metadata = [
        {
            "id": idx,
            "original_question": "",
            "easy_question": "",
            "answer": answer,
            "search_text": "",
        }
        for idx, answer in enumerate(_answers)
    ]

# 용어집 딕셔너리 (terms_dataset -> 프롬프트 주입용)
_terms_df = pd.read_csv(TERMS_PATH, encoding="utf-8-sig").fillna("")
TERMS_DICT: dict[str, str] = dict(zip(_terms_df["단어"], _terms_df["단순화"]))

print(f"[retriever] 로드 완료: 벡터 {_index.ntotal}개, 용어{len(TERMS_DICT)}개")


def retrieve_top_k(query: str, top_k: int = DEFAULT_TOP_K, 
             threshold: float = DEFAULT_THRESHOLD) -> list[dict]:
    """
    사용자 질문을 받아 가장 유사한 답변을 top-k개 반환합니다.

    Returns:
        [
            {
                "rank": 1,
                "score": 0.8123,
                "original_question": "...",
                "easy_question": "...",
                "answer": "...",
                "search_text": "..."
            }
        ]
    """
    if not query or not query.strip():
        return []

    vec = _model.encode([query], normalize_embeddings=True)
    vec = np.array(vec, dtype="float32")

    scores, indices = _index.search(vec, top_k)

    results = []
    for score, index_id in zip(scores[0], indices[0]):
        score = float(score)
        index_id = int(index_id)

        if index_id < 0:
            continue

        if score < threshold:
            continue

        item = _metadata[index_id]
        results.append(
            {
                "rank": len(results) + 1,
                "score": score,
                "original_question": item.get("original_question", ""),
                "easy_question": item.get("easy_question", ""),
                "answer": item.get("answer", _answers[index_id]),
                "search_text": item.get("search_text", ""),
            }
        )

    return results

def retrieve(
    query: str,
    top_k: int = 1,
    threshold: float = DEFAULT_THRESHOLD,
) -> str:
    """
    기존 백엔드 연동을 위한 단순 함수입니다.
    가장 유사한 FAQ 답변 1개만 문자열로 반환합니다.
    """
    results = retrieve_top_k(query, top_k=top_k, threshold=threshold)

    if not results:
        return FALLBACK_ANSWER

    return results[0]["answer"]

def get_rag_context(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    threshold: float = DEFAULT_THRESHOLD,
) -> str:
    """
    LLM 프롬프트에 바로 넣을 수 있는 RAG context 문자열을 반환합니다.
    백엔드 담당자는 이 함수를 main.py에서 사용하는 것을 권장합니다.
    """
    results = retrieve_top_k(query, top_k=top_k, threshold=threshold)

    if not results:
        return "관련 FAQ 자료를 찾지 못했습니다."

    context_blocks = []
    for item in results:
        context_blocks.append(
            f"[FAQ 후보 {item['rank']}]\n"
            f"유사도: {item['score']:.3f}\n"
            f"원문 질문: {item['original_question']}\n"
            f"쉬운 질문: {item['easy_question']}\n"
            f"답변: {item['answer']}"
        )

    return "\n\n".join(context_blocks)

def retrieve_debug(query: str, top_k: int = 5) -> dict:
    """
    개발/디버깅용 함수입니다.
    threshold를 0으로 두고 검색 후보를 확인합니다.
    """
    return {
        "query": query,
        "top_k": top_k,
        "results": retrieve_top_k(query, top_k=top_k, threshold=0.0),
    }

def get_terms_context(limit: int | None = None) -> str:
    """
    용어집을 LLM 프롬프트에 삽입할 문자열로 반환합니다.
    """
    items = list(TERMS_DICT.items())
    
    if limit is not None:
        items = items[:limit]

    lines = [f"{term} → {easy}" for term, easy in items]
    return "\n".join(lines)

def simplify_terms(text: str) -> str:
    """
    terms_dataset.csv 기반으로 문장 안의 의료용어를 쉬운 표현으로 치환합니다.
    test_cases.csv는 이 함수 또는 LLM 쉬운말 변환 평가에 더 적합합니다.
    """
    if not text:
        return ""

    result = text

    sorted_terms = sorted(TERMS_DICT.items(), key=lambda item: len(item[0]), reverse=True)
    for term, easy in sorted_terms:
        if term in result:
            result = result.replace(term, easy)

    return result