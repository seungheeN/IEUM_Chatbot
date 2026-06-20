"""
embed.py 실행 후 이 파일로 동작을 확인합니다.
실행: python rag/test_rag.py

중요:
- qa_dataset.csv는 FAQ 검색용 데이터입니다.
- test_cases.csv는 FAQ 검색 평가셋이 아니라 의료문장 쉬운말 변환 데이터입니다.

"""

import os
import sys
import pandas as pd

# rag/ 폴더를 기준으로 import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from retriever import (
    get_rag_context,
    get_terms_context,
    retrieve,
    retrieve_debug,
    retrieve_top_k,
    simplify_terms,
)

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
QA_PATH = os.path.join(DATA_DIR, "qa_dataset.csv")
TEST_CASES_PATH = os.path.join(DATA_DIR, "test_cases.csv")

def test_faq_retrieval():
    """
    qa_dataset.csv 기준 FAQ 검색 테스트입니다.
    같은 데이터로 만든 인덱스를 다시 검색하는 smoke test입니다.
    """
    qa_df = pd.read_csv(QA_PATH, encoding="utf-8-sig").fillna("")

    print(f"=== FAQ 검색 테스트 ({len(qa_df)}건) ===")

    correct = 0

    for _, row in qa_df.iterrows():
        query = row["쉬운 질문"]
        expected_answer = row["답변"]
        result = retrieve(query)

        is_match = expected_answer == result
        mark = "PASS" if is_match else "CHECK"

        if is_match:
            correct += 1

        print(f"[{mark}] 질문: {query}")
        print(f"       예상: {expected_answer}")
        print(f"       결과: {result}")
        print()

    print(f"FAQ 검색 결과: {correct}/{len(qa_df)} 정확히 일치")
    print()


def test_top_k_sample():
    """
    top-k 검색 결과와 score 확인용 샘플입니다.
    """
    sample_queries = [
        "병원 처음 가면 어떻게 해야 하나요?",
        "진료비는 어디서 내나요?",
        "입원 절차 알려주세요.",
        "처방전은 어디서 받나요?",
    ]

    print("=== top-k 검색 샘플 ===")

    for query in sample_queries:
        print(f"질문: {query}")
        results = retrieve_top_k(query, top_k=3, threshold=0.0)

        for item in results:
            print(
                f"  {item['rank']}. score={item['score']:.3f} / "
                f"질문={item['original_question']} / 답변={item['answer']}"
            )

        print()


def test_rag_context_sample():
    """
    백엔드 LLM 프롬프트에 넣을 context 형태 확인용입니다.
    """
    query = "수납은 어디서 하나요?"

    print("=== RAG context 샘플 ===")
    print(f"질문: {query}")
    print(get_rag_context(query, top_k=3))
    print()


def test_term_simplification():
    """
    test_cases.csv는 retrieve() 평가가 아니라 쉬운말 변환 평가에 가깝습니다.
    여기서는 terms_dataset.csv 기반 단순 치환 결과를 확인합니다.
    """
    test_df = pd.read_csv(TEST_CASES_PATH, encoding="utf-8-sig").fillna("")

    print(f"=== 의료문장 쉬운말 변환 샘플 ({len(test_df)}건) ===")

    for _, row in test_df.head(10).iterrows():
        source = row["입력"]
        expected = row["예상출력"]
        simplified = simplify_terms(source)

        print(f"입력: {source}")
        print(f"예상: {expected}")
        print(f"치환: {simplified}")
        print()


def check_terms():
    print("=== 용어집 샘플 ===")
    print(get_terms_context(limit=10))
    print()


def debug_sample():
    print("=== 디버그 샘플 ===")
    debug_result = retrieve_debug("MRI 촬영 전에 밥 먹어도 되나요?", top_k=5)
    print(debug_result)
    print()


if __name__ == "__main__":
    check_terms()
    test_faq_retrieval()
    test_top_k_sample()
    test_rag_context_sample()
    test_term_simplification()
    debug_sample()