import Message from "./Message";

function ChatWindow({ messages, loading }) {
  return (
    <div
      style={{
        border: "1px solid #d9e2f1",
        borderRadius: "16px",
        padding: "16px",
        height: "420px",
        overflowY: "auto",
        backgroundColor: "#f9fbff",
        marginBottom: "12px"
      }}
    >
      {messages.map((msg, index) => (
        <Message key={index} role={msg.role} text={msg.text} />
      ))}

      {loading && (
        <div style={{ textAlign: "left", margin: "8px 0" }}>
          <span
            style={{
              display: "inline-block",
              backgroundColor: "#e5e7eb",
              color: "#111827",
              padding: "12px 16px",
              borderRadius: "14px",
              fontSize: "18px"
            }}
          >
            답변을 불러오는 중입니다...
          </span>
        </div>
      )}
    </div>
  );
}

export default ChatWindow;

