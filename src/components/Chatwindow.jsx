import Message from "./Message";

function ChatWindow({ messages }) {
  return (
    <div style={{
      border: "1px solid #ccc",
      borderRadius: "10px",
      height: "450px",
      padding: "16px",
      overflowY: "scroll",
      backgroundColor: "#fafafa"
    }}>
      {messages.map((msg, index) => (
        <Message key={index} msg={msg} />
      ))}
    </div>
  );
}

export default ChatWindow;
