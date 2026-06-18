import { useState } from "react";
import MainScreen from "./components/MainScreen";
import ChatWindow from "./components/Chatwindow";
import InputBar from "./components/Inputbar";
import VoiceControls from "./components/VoiceControls";
import "./App.css";

function App() {
  const [screen, setScreen] = useState("main");
  const [messages, setMessages] = useState([
    { role: "bot", text: "안녕하세요. 무엇을 도와드릴까요?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  const API_BASE_URL = "http://localhost:8000";

  const stopSpeaking = () => {
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
  };

  const speakText = (text) => {
    if (!text) return;

    stopSpeaking();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "ko-KR";
    utterance.rate = 0.9;
    utterance.pitch = 1;

    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    setIsSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  const sendMessage = async (messageText = input, speakResponse = false) => {
    if (!messageText.trim() || loading) return;

    const userText = messageText.trim();

    setMessages((prev) => [...prev, { role: "user", text: userText }]);
    setInput("");
    setLoading(true);
    stopSpeaking();

    try {
      const res = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ session_id: "user_default", prompt: userText })
      });

      if (!res.ok) {
        throw new Error("chat api error");
      }

      const data = await res.json();
      const botText = data.response || "답변을 불러오지 못했습니다.";

      setMessages((prev) => [
        ...prev,
        { role: "bot", text: botText }
      ]);

      if (speakResponse) {
        speakText(botText);
      }
    } catch {
      const errorMessage = "서버와 연결되지 않았습니다. 잠시 후 다시 시도해 주세요.";

      setMessages((prev) => [
        ...prev,
        { role: "bot", text: errorMessage }
      ]);

      if (speakResponse) {
        speakText(errorMessage);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSpeechResult = (recognizedText) => {
    setInput(recognizedText);
    sendMessage(recognizedText, true);
  };

  const speakLastBotMessage = () => {
    const lastBotMessage = [...messages].reverse().find((msg) => msg.role === "bot");

    if (!lastBotMessage) return;

    speakText(lastBotMessage.text);
  };

  if (screen === "main") {
    return <MainScreen onChatStart={() => setScreen("chat")} />;
  }

  return (
    <div
      style={{
        maxWidth: "600px",
        margin: "0 auto",
        padding: "20px"
      }}
    >
      <button
        onClick={() => setScreen("main")}
        style={{
          fontSize: "18px",
          marginBottom: "10px",
          background: "none",
          border: "none",
          cursor: "pointer",
          color: "#1a3a6b"
        }}
      >
        ← 뒤로가기
      </button>

      <h2
        style={{
          fontSize: "24px",
          textAlign: "center",
          color: "#1a3a6b"
        }}
      >
        병원 안내 챗봇
      </h2>

      <ChatWindow messages={messages} loading={loading} />

      <VoiceControls
        onSpeechResult={handleSpeechResult}
        onSpeak={speakLastBotMessage}
        onStopSpeak={stopSpeaking}
        isSpeaking={isSpeaking}
        loading={loading}
      />

      <InputBar
        input={input}
        setInput={setInput}
        onSend={() => sendMessage()}
        loading={loading}
      />
    </div>
  );
}

export default App;
