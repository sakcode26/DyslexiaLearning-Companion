import React, { useState } from "react";
import { Routes, Route, Link, useLocation } from "react-router-dom";
import DyslexiaPage from "./DyslexiaPage";
import AutismPage from "./AutismPage";
import WritingAssistant from "./WritingAssistant";
import LettersLearning from "./LettersLearning";
import ReadingAssistant from "./ReadingAssistant";

function App() {
  const [showButtons, setShowButtons] = useState(false);
  const location = useLocation(); // ✅ Gets the current route

  return (
    <div style={styles.container}>
      {/* ✅ Only show the welcome section if on the home page */}
      {location.pathname === "/" && (
        <>
          <h1 style={styles.heading}>DYSLEXIA LEARNING COMPANION</h1>

          {!showButtons ? (
            <button style={styles.welcomeButton} onClick={() => setShowButtons(true)}>
              Welcome
            </button>
          ) : (
            <div style={styles.buttonContainer}>
              <Link to="/dyslexia">
                <button style={styles.optionButton}>Dyslexia</button>
              </Link>
              <Link to="/autism">
                <button style={styles.optionButton}>Autism</button>
              </Link>
            </div>
          )}

          <div style={styles.imageContainer}>
            <img src="dyslexia1.jpg" alt="Dyslexia Awareness" style={styles.image} />
          </div>
        </>
      )}

      {/* ✅ Routes - Handles Page Navigation */}
      <Routes>
        <Route path="/dyslexia" element={<DyslexiaPage />} />
        <Route path="/autism" element={<AutismPage />} />
        <Route path="/writing-assistant" element={<WritingAssistant />} />
        <Route path="/letters-learning" element={<LettersLearning />} />
        <Route path="/reading-assistant" element={<ReadingAssistant />} />
      </Routes>
    </div>
  );
}

const styles = {
  container: {
    textAlign: "center",
    background: "linear-gradient(to right, #000428, #004e92)",
    height: "100vh",
    color: "white",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
  },
  heading: { fontSize: "2.5rem", marginBottom: "20px" },
  welcomeButton: {
    fontSize: "1.2rem",
    padding: "10px 20px",
    backgroundColor: "#ff9800",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },
  buttonContainer: { display: "flex", gap: "15px", marginTop: "20px" },
  optionButton: {
    fontSize: "1.2rem",
    padding: "10px 20px",
    backgroundColor: "#ff5722",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    textDecoration: "none",
    color: "white",
  },
  imageContainer: { marginTop: "30px", display: "flex", gap: "15px" },
  image: { width: "200px", height: "150px", borderRadius: "10px" },
};

export default App;
