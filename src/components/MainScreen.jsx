function MainScreen({ onChatStart }) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "space-between",
        height: "100vh",
        backgroundColor: "#f0f4ff",
        padding: "40px 20px",
        boxSizing: "border-box"
      }}
    >
      <div style={{ textAlign: "center" }}>
        <div style={{ fontSize: "40px" }}>🏥</div>
        <h1
          style={{
            fontSize: "28px",
            fontWeight: "bold",
            color: "#1a3a6b",
            marginTop: "10px"
          }}
        >
          병원 안내 챗봇
        </h1>
        <p
          style={{
            fontSize: "18px",
            color: "#555",
            marginTop: "8px"
          }}
        >
          무엇이든 물어보세요!
        </p>
      </div>

      <div style={{ textAlign: "center" }}>
        <button
          onClick={onChatStart}
          style={{
            width: "160px",
            height: "160px",
            borderRadius: "50%",
            backgroundColor: "#1a3a6b",
            border: "none",
            fontSize: "60px",
            cursor: "pointer",
            boxShadow: "0 6px 20px rgba(0,0,0,0.2)"
          }}
        >
          🎤
        </button>
        <p
          style={{
            fontSize: "20px",
            color: "#1a3a6b",
            marginTop: "16px",
            fontWeight: "bold"
          }}
        >
          말씀하세요
        </p>
      </div>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "16px",
          width: "100%",
          maxWidth: "400px"
        }}
      >
        <button
          onClick={onChatStart}
          style={{
            padding: "20px",
            fontSize: "20px",
            fontWeight: "bold",
            backgroundColor: "#ffffff",
            color: "#1a3a6b",
            border: "2px solid #1a3a6b",
            borderRadius: "16px",
            cursor: "pointer"
          }}
        >
          ✏️ 글로 질문하기
        </button>

        <button
          onClick={() => alert("자주 묻는 질문 기능은 준비 중입니다.")}
          style={{
            padding: "20px",
            fontSize: "20px",
            fontWeight: "bold",
            backgroundColor: "#ffffff",
            color: "#1a3a6b",
            border: "2px solid #1a3a6b",
            borderRadius: "16px",
            cursor: "pointer"
          }}
        >
          📋 자주 묻는 질문
        </button>
      </div>
    </div>
  );
}

export default MainScreen;

