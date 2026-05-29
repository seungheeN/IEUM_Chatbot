import { useState } from "react";
import ChatWindow from "./components/Chatwindow";
import InputBar from "./components/Inputbar";

function App() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "안녕하세요 😊 무엇을 도와드릴까요?" }
  ]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: "user", text: input }]);
    setInput("");
  };

  return (
    <div style={{
      maxWidth: "600px",
      margin: "0 auto",
      padding: "20px"
    }}>
      <h1 style={{ fontSize: "28px", textAlign: "center" }}>
        🏥 병원 안내 챗봇
      </h1>
      <ChatWindow messages={messages} />
      <InputBar input={input} setInput={setInput} onSend={sendMessage} />
    </div>
  );
}

export default App;
