import { useEffect, useRef } from "react";
import Message from "./Message";

function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <section className="chat-window" aria-live="polite">
      {messages.length === 0 ? (
        <div className="empty-state">질문을 입력하면 여기에서 답변을 볼 수 있습니다.</div>
      ) : (
        messages.map((msg, index) => <Message key={`${msg.role}-${index}`} role={msg.role} text={msg.text} />)
      )}

      {loading && (
        <div className="message-row bot-row">
          <div className="message bot-message loading-bubble">
            <span className="loading-dot" />
            <span className="loading-dot" />
            <span className="loading-dot" />
            <span className="loading-text">답변을 준비하고 있습니다.</span>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </section>
  );
}

export default ChatWindow;
