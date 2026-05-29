function Message({ msg }) {
  const isUser = msg.role === "user";

  return (
    <div style={{
      display: "flex",
      justifyContent: isUser ? "flex-end" : "flex-start",
      marginBottom: "10px"
    }}>
      <div style={{
        backgroundColor: isUser ? "#4CAF50" : "#f1f1f1",
        color: isUser ? "white" : "black",
        padding: "12px 16px",
        borderRadius: "18px",
        maxWidth: "70%",
        fontSize: "18px"
      }}>
        {msg.text}
      </div>
    </div>
  );
}

export default Message;
