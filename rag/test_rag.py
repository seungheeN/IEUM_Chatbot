"""
embed.py 실행 후 이 파일로 동작을 확인합니다.
실행: python rag/test_rag.py
"""

import os
import sys
import pandas as pd

# rag/ 폴더를 기준으로 import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from retriever import retrieve, get_terms_context

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
TEST_PATH = os.path.join(BASE_DIR, "data", "test_cases.csv")


def run_tests():
    test_df = pd.read_csv(TEST_PATH)
    print(f"=== RAG 동작 테스트 ({len(test_df)}건) ===\n")

    correct = 0
    for _, row in test_df.iterrows():
        query    = row["입력"]
        expected = row["예상출력"]
        result   = retrieve(query)

        match = "✅" if expected in result or result in expected else "🔍"
        if match == "✅":
            correct += 1

        print(f"[{match}] 입력:  {query}")
        print(f"      예상:  {expected}")
        print(f"      결과:  {result}")
        print()

    print(f"결과: {correct}/{len(test_df)} 일치")


def check_terms():
    context = get_terms_context()
    print("=== 용어집 샘플 (상위 5개) ===")
    print("\n".join(context.split("\n")[:5]))
    print()


if __name__ == "__main__":
    check_terms()
    run_tests()