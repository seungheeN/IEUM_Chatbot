function VoiceControls({ onSpeechResult, onSpeak }) {
  const startSTT = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("이 브라우저에서는 음성 입력이 지원되지 않습니다. 크롬에서 실행해 주세요.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "ko-KR";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      onSpeechResult(text);
    };

    recognition.onerror = () => {
      alert("음성 인식 중 오류가 발생했습니다.");
    };
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
        onClick={startSTT}
        style={{
          fontSize: "18px",
          padding: "12px 16px",
          borderRadius: "12px",
          border: "none",
          backgroundColor: "#34a853",
          color: "white",
          cursor: "pointer"
        }}
      >
        🎤 음성 입력
      </button>

      <button
        onClick={onSpeak}
        style={{
          fontSize: "18px",
          padding: "12px 16px",
          borderRadius: "12px",
          border: "none",
          backgroundColor: "#7e57c2",
          color: "white",
          cursor: "pointer"
        }}
      >
        🔊 답변 읽기
      </button>
    </div>
  );
}

export default VoiceControls;
