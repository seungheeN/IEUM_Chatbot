function InputBar({ input, setInput, onSend }) {
  return (
    <div style={{
      display: "flex",
      gap: "10px",
      marginTop: "10px"
    }}>
      <input
        type="text"
        placeholder="질문을 입력하세요"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && onSend()}
        style={{
          flex: 1,
          padding: "14px",
          fontSize: "18px",
          borderRadius: "10px",
          border: "1px solid #ccc"
        }}
      />
      <button
        onClick={onSend}
        style={{
          padding: "14px 20px",
          fontSize: "18px",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "10px",
          cursor: "pointer"
        }}
      >
        전송
      </button>
    </div>
  );
}

export default InputBar;
