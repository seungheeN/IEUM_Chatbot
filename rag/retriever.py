"""
백엔드 담당자가 import해서 사용할 파일입니다.
공개 인터페이스: retrieve(query) -> str
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

MODEL_NAME = "snunlp/KR-SBERT-V40K-klueNLI-augSTS"

# 모듈 로드 시 1회만 초기화
print("[retriever] 모델 및 인덱스 로드 중...")
_model = SentenceTransformer(MODEL_NAME)

_index = faiss.read_index(INDEX_PATH)

with open(ANSWERS_PATH, "rb") as f:
    _answers = pickle.load(f)

# 용어집 딕셔너리 (terms_dataset -> 프롬프트 주입용)
_terms_df = pd.read_csv(TERMS_PATH)
TERMS_DICT: dict[str, str] = dict(zip(_terms_df["단어"], _terms_df["단순화"]))

print(f"[retriever] 로드 완료: 벡터 {_index.ntotal}개, 용어 {len(TERMS_DICT)}개")


def retrieve(query: str, top_k: int = 1, threshold: float = 0.2) -> str:
    """
    사용자 질문을 받아 가장 유사한 답변을 반환합니다.

    Parameters
    ----------
    query     : 사용자 질문 문자열
    top_k     : 검색할 후보 수 (기본값 1)
    threshold : 유사도 최소값. 이 값 미만이면 기본 답변 반환 (기본값 0.5)

    Returns
    -------
    str : 검색된 답변 또는 기본 안내 문구
    """
    vec = _model.encode([query], normalize_embeddings=True)
    vec = np.array(vec, dtype="float32")

    scores, indices = _index.search(vec, top_k)
    top_score = float(scores[0][0])
    top_index = int(indices[0][0])

    if top_score < threshold:
        return "죄송합니다. 해당 질문에 대한 답변을 찾지 못했습니다. 접수 창구에 직접 문의해 주세요."

    return _answers[top_index]


def get_terms_context() -> str:
    """
    용어집을 LLM 프롬프트에 삽입할 문자열로 반환합니다.
    백엔드 담당자가 system prompt 구성 시 사용합니다.

    Returns
    -------
    str : '단어 → 쉬운표현' 형식의 줄바꿈 문자열
    """
    lines = [f"{k} → {v}" for k, v in TERMS_DICT.items()]
    return "\n".join(lines)