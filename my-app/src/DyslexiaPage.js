import React from "react";
import { Link } from "react-router-dom";

function DyslexiaPage() {
  const handleRunReadingAssistant = async () => {
    try {
      const response = await fetch("http://localhost:5000/run-reading-assistant");
      const data = await response.json();
      alert(data.message); // Show success message
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to execute Reading Assistant");
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Dyslexia Learning Modules</h1>
      <div style={styles.buttonContainer}>
        <button onClick={handleRunReadingAssistant} style={styles.optionButton}>
          📖 Reading Assistant
        </button>
        <Link to="/writing-assistant">
          <button style={styles.optionButton}>✍️ Writing Assistant</button>
        </Link>
        <Link to="/letters-learning">
          <button style={styles.optionButton}>🔤 Letters Learning</button>
        </Link>
      </div>
    </div>
  );
}

const styles = {
  container: {
    textAlign: "center",
    background: "#222",
    height: "100vh",
    color: "white",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
  },
  heading: { fontSize: "2.5rem", marginBottom: "20px" },
  buttonContainer: { display: "flex", gap: "15px", marginTop: "20px" },
  optionButton: {
    fontSize: "1.2rem",
    padding: "10px 20px",
    backgroundColor: "#ff5722",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    color: "white",
  },
};

export default DyslexiaPage;
