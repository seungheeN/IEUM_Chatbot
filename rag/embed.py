"""
최초 1회 또는 qa_dataset.csv 변경 시 실행합니다.
실행: python rag/embed.py

결과:
- rag/store/vector_store.index
- rag/store/answers.pkl
- rag/store/metadata.pkl
"""

import os
import pickle
import numpy as np
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STORE_DIR = os.path.join(BASE_DIR, "store")
os.makedirs(STORE_DIR, exist_ok=True)

QA_PATH = os.path.join(DATA_DIR, "qa_dataset.csv")

INDEX_PATH = os.path.join(STORE_DIR, "vector_store.index")
ANSWERS_PATH = os.path.join(STORE_DIR, "answers.pkl")
METADATA_PATH = os.path.join(STORE_DIR, "metadata.pkl")

# 한국어 SBERT 모델
MODEL_NAME = "snunlp/KR-SBERT-V40K-klueNLI-augSTS"


def build_index():
    # 1. 데이터 로드
    qa_df = pd.read_csv(QA_PATH, encoding="utf-8-sig")
    qa_df = qa_df.fillna("")

    required_columns = {"원문 질문", "쉬운 질문", "답변"}
    missing_columns = required_columns - set(qa_df.columns)
    if missing_columns:
        raise ValueError(f"qa_dataset.csv에 필요한 컬럼이 없습니다: {missing_columns}")
    
    print(f"[embed] QA 데이터 로드 완료: {len(qa_df)}행")

    # 2. 검색용 텍스트 생성 (원문 질문 + 쉬운 질문 합치기)
    qa_df["검색용"] = (qa_df["원문 질문"].astype(str) + " " 
                    + qa_df["쉬운 질문"].astype(str) + " " 
                    + qa_df["답변"].astype(str))
    
    queries = qa_df["검색용"].tolist()
    answers = qa_df["답변"].tolist()

    metadata = []
    for idx, row in qa_df.iterrows():
        metadata.append(
            {
                "id": int(idx),
                "original_question": row["원문 질문"],
                "easy_question": row["쉬운 질문"],
                "answer": row["답변"],
                "search_text": row["검색용"],
            }
        )

    # 3. 임베딩
    print(f"[embed] 모델 로드 중: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    print("[embed] 임베딩 생성 중...")
    embeddings = model.encode(
        queries,
        normalize_embeddings=True,  # 코사인 유사도 대신 내적으로 계산 가능하게
        show_progress_bar=True
    )
    embeddings = np.array(embeddings, dtype="float32")

    # 4. FAISS 인덱스 생성
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # 내적(Inner Product) = 정규화된 벡터의 코사인 유사도
    index.add(embeddings)
    print(f"[embed] 인덱스 생성 완료: {index.ntotal}개 벡터, 차원={dim}")

    # 5. 저장
    faiss.write_index(index, INDEX_PATH)
    with open(ANSWERS_PATH, "wb") as f:
        pickle.dump(answers, f)

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)
        
    print(f"[embed] 저장 완료")
    print(f"  - 인덱스: {INDEX_PATH}")
    print(f"  - 답변:   {ANSWERS_PATH}")
    print(f"  - metadata: {METADATA_PATH}")


if __name__ == "__main__":
    build_index()