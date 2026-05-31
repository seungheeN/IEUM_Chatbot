import { useState } from "react";
import MainScreen from "./components/MainScreen";
import ChatWindow from "./components/Chatwindow";
import InputBar from "./components/Inputbar";

function App() {
  const [screen, setScreen] = useState("main");
  const [messages, setMessages] = useState([
    { role: "bot", text: "안녕하세요 😊 무엇을 도와드릴까요?" }
  ]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: "user", text: input }]);
    setInput("");
  };

  if (screen === "main") {
    return <MainScreen onChatStart={() => setScreen("chat")} />;
  }

  return (
    <div style={{
      maxWidth: "600px",
      margin: "0 auto",
      padding: "20px"
    }}>
      <button
        onClick={() => setScreen("main")}
        style={{
          fontSize: "18px",
          marginBottom: "10px",
          background: "none",
          border: "none",
          cursor: "pointer",
          color: "#1a3a6b"
        }}>
        ← 뒤로가기
      </button>
      <h2 style={{ fontSize: "24px", textAlign: "center", color: "#1a3a6b" }}>
        🏥 병원 안내 챗봇
      </h2>
      <ChatWindow messages={messages} />
      <InputBar input={input} setInput={setInput} onSend={sendMessage} />
    </div>
  );
}

export default App;
