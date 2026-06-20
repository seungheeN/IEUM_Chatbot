import { useRef, useState } from "react";

function VoiceControls({ onSpeechResult, onSpeak, onStopSpeak, isSpeaking, loading }) {
  const recognitionRef = useRef(null);
  const [listening, setListening] = useState(false);

  const startSTT = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("이 브라우저에서는 음성 입력이 지원되지 않습니다. Chrome에서 실행해 주세요.");
      return;
    }

    if (listening || loading) return;

    const recognition = new SpeechRecognition();
    recognition.lang = "ko-KR";
    recognition.interimResults = false;
    recognition.continuous = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setListening(true);
    };

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript.trim();
      if (text) {
        onSpeechResult(text);
      }
    };

    recognition.onerror = () => {
      alert("음성 인식 중 오류가 발생했습니다. 마이크 권한을 확인해 주세요.");
    };

    recognition.onend = () => {
      setListening(false);
      recognitionRef.current = null;
    };

    recognitionRef.current = recognition;
    recognition.start();
  };

  const stopSTT = () => {
    recognitionRef.current?.stop();
  };

  return (
    <div
      style={{
        display: "flex",
        gap: "10px",
        marginBottom: "10px"
      }}
    >
      <button
        onClick={listening ? stopSTT : startSTT}
        disabled={loading}
        style={{
          fontSize: "18px",
          padding: "12px 16px",
          borderRadius: "12px",
          border: "none",
          backgroundColor: listening ? "#d93025" : "#34a853",
          color: "white",
          cursor: loading ? "not-allowed" : "pointer"
        }}
      >
        {listening ? "음성 입력 중지" : "음성 입력"}
      </button>

      <button
        onClick={isSpeaking ? onStopSpeak : onSpeak}
        disabled={loading}
        style={{
          fontSize: "18px",
          padding: "12px 16px",
          borderRadius: "12px",
          border: "none",
          backgroundColor: isSpeaking ? "#5f6368" : "#7e57c2",
          color: "white",
          cursor: loading ? "not-allowed" : "pointer"
        }}
      >
        {isSpeaking ? "읽기 중지" : "답변 읽기"}
      </button>
    </div>
  );
}

export default VoiceControls;