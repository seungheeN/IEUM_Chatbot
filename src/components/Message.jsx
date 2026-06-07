function Message({ role, text }) {
  const isUser = role === "user";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        margin: "8px 0"
      }}
    >
      <div
        style={{
          maxWidth: "75%",
          backgroundColor: isUser ? "#c7f7d4" : "#e8eef9",
          color: "#222",
          padding: "12px 16px",
          borderRadius: "16px",
          fontSize: "18px",
          lineHeight: "1.5"
        }}
      >
        {text}
      </div>
    </div>
  );
}

export default Message;
