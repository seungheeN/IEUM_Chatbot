function InputBar({ input, setInput, onSend, loading }) {
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !loading) {
      onSend();
    }
  };

  return (
    <div
      style={{
        display: "flex",
        gap: "10px",
        marginTop: "10px"
      }}
    >
      <input
        type="text"
        value={input}
        placeholder="질문을 입력해 주세요"
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={loading}
        style={{
          flex: 1,
          fontSize: "18px",
          padding: "14px",
          borderRadius: "12px",
          border: "1px solid #b8c7e0"
        }}
      />
      <button
        onClick={onSend}
        disabled={loading}
        style={{
          fontSize: "18px",
          padding: "14px 18px",
          borderRadius: "12px",
          border: "none",
          backgroundColor: "#1a73e8",
          color: "white",
          cursor: loading ? "not-allowed" : "pointer"
        }}
      >
        전송
      </button>
    </div>
  );
}

export default InputBar;
