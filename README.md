# 🏥 IEUM Chatbot (이음 챗봇)
**어르신 맞춤형 로컬 병원 안내 AI**

디지털 소외계층인 어르신들이 병원 이용 절차와 위치를 쉽고 편하게 안내받을 수 있도록 돕는 **로컬 LLM 기반 음성/텍스트 안내 챗봇 서비스**입니다. 외부 API(OpenAI 등) 의존 없이 자체 파인튜닝된 모델과 RAG(검색 증강 생성)를 결합하여, 로컬 CPU 및 내장 그래픽 환경에서도 안전하고 빠르게 구동됩니다.

---

## 👥 팀원 및 역할
| 이름 | 담당 분야 | 세부 역할 및 기여 내역 |
|:----:|:---|:---|
| **노승희** | **Backend & AI** | FastAPI 서빙 환경 구축, RAG 검색 모듈 통합, CPU 최적화, QLoRA 파인튜닝 파이프라인 설계 |
| **현아림** | **Data Engineering** | 병원 안내 QA 데이터셋 구축, 엣지 케이스 시나리오 기획 및 데이터 보강(Enrichment) |
| **황희성** | **Backend & Frontend** | 어르신 친화적 웹/앱 UI 구현, TTS(음성 출력) 모듈 연동, 백엔드 API 비동기 통신 구현, 데모 영상 제작 |

---

## 💡 주요 기능
*  **어르신 맞춤형 페르소나:** QLoRA 파인튜닝을 통해 친절한 어조로 명확하게 안내합니다.
*  **환각(Hallucination) 방어:** 병원 안내 엑셀 데이터에 기반한 RAG 기술과 정규식 기반 폴백(Fallback) 로직으로 잘못된 의료 정보 생성을 차단합니다.
*  **초경량 로컬 서빙:** 무거운 외장 GPU 없이 4-bit GGUF 양자화 모델과 CPU 멀티스레딩 최적화를 통해 20초대의 응답 속도를 제공합니다.
*  **음성 / 텍스트 입출력:** TTS 모듈 연동을 통해 화면의 텍스트뿐만 아니라 자연스러운 음성 안내를 동시에 지원합니다.

---

## 🛠 기술 스택

| 분류 | 사용 기술 |
|:---|:---|
| **AI Model** | **Base:** `Qwen2.5-3B-Korean.Q4_K_M.gguf`<br>**Final (Tuned):** `qwen2.5-3b-instruct.Q4_K_M.gguf` |
| **Fine-Tuning** | Unsloth, PEFT, QLoRA (Google Colab T4 GPU 환경) |
| **Backend** | FastAPI, llama-cpp-python, Python 3.10+ |
| **RAG System** | FAISS Vector Store, Custom Regex Filter, In-Memory Sliding Window |
| **Frontend** | React, Web TTS API |

---

## 📁 프로젝트 구조
```text
IEUM_Chatbot/
│
├── main.py                     # FastAPI 앱 진입점 & 서버 실행
├── requirements.txt            # 패키지 의존성
├── prompt_design.txt           # 시스템 프롬프트 설계
├── train_model.ipynb           # QLoRA 파인튜닝 노트북 (Colab)
├── hospital_location.csv       # 병원 위치 데이터
├── qa_dataset.csv              # 학습용 QA 데이터셋
├── terms_dataset.csv           # 의료 용어 데이터셋
├── retrieve_testset.csv        # RAG 검색 테스트셋
│
├── rag/                        # RAG 파이프라인
│   ├── embed.py                # 문서 임베딩 생성
│   ├── retriever.py            # 벡터 검색 모듈
│   ├── test_rag.py             # RAG 성능 테스트
│   ├── data/                   # RAG 원본 데이터
│   │   ├── qa_dataset.csv
│   │   ├── terms_dataset.csv
│   │   └── test_cases.csv
│   └── store/                  # 생성된 벡터스토어 (임베딩 캐시)
│       ├── answers.pkl
│       ├── metadata.pkl
│       └── vector_store.index
│
└── src/                        # React 프론트엔드
    ├── App.jsx                 # 앱 루트 컴포넌트
    └── components/
        ├── ChatWindow.jsx      # 채팅 화면
        ├── Inputbar.jsx        # 텍스트 입력창
        ├── MainScreen.jsx      # 메인 화면
        ├── Message.jsx         # 메시지 말풍선
        └── VoiceControls.jsx   # 음성 입출력 컨트롤
```

## 🚀 시작 가이드
> 사전 요구 사항
- Python 3.10 이상
- Node.js 18 이상 (프론트엔드 실행 시)
- 외장 GPU 불필요: 일반 노트북(CPU) 환경에서 동작하도록 최적화되어 있습니다.

**1. 저장소 클론 및 패키지 설치**

터미널을 열고 아래 명령어를 순서대로 실행하여 프로젝트를 클론하고 의존성 패키지를 설치합니다.

```text
git clone https://github.com/seungheeN/IEUM_Chatbot.git
cd IEUM_Chatbot
pip install -r requirements.txt
```
**2. 파인튜닝 모델 파일 다운로드**

최종 서빙용 모델 파일(qwen2.5-3b-instruct.Q4_K_M.gguf)은 용량 문제로 GitHub 저장소에 포함되어 있지 않습니다. 아래 링크에서 다운로드 후 프로젝트 루트 폴더에 배치해 주세요.

> <https://drive.google.com/file/d/1xmKsFtNZw048PYMnutkgE19tywWn4GgA/view?usp=sharing>

**3. 벡터스토어 생성 (최초 1회)**


초기 데이터베이스 구축을 위해 아래 명령어를 실행합니다. rag/store/ 폴더에 벡터 인덱스 파일이 자동으로 생성됩니다.

```text
python rag/embed.py
```
**4. 백엔드 서버 실행**

아래 명령어를 통해 FastAPI 기반의 백엔드 서버를 구동합니다.

```text
uvicorn main:app --reload --port 8000
(서버가 성공적으로 실행되면 터미널에 모델 로드 완료 메시지가 출력됩니다.)
```

**5. 프론트엔드 실행**


새로운 터미널 창을 열고 프론트엔드 폴더로 이동하여 웹 서버를 구동합니다.

```text
cd src
npm install
npm start
```

이후 브라우저에서 <http://localhost:3000>에 접속하여 챗봇 서비스를 이용하실 수 있습니다.
