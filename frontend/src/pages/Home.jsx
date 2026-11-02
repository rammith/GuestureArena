
import { useNavigate } from "react-router-dom";
import "../styles/Home.css";

function Home() {
  const navigate = useNavigate();

  const handleStartGame = () => {
    navigate("/game");
  };

  const handleGameHistory = () => {
    navigate("/history");
  };

  return (
    <div className="home-container">

      <nav className="home-navbar">
        <div className="logo">
          <span className="logo-icon">✊</span>
          <span>
            Gesture<span className="logo-highlight">Play</span>
          </span>
        </div>

        <div className="nav-label">
          AI POWERED GAMING
        </div>
      </nav>

      <main className="home-content">

        <div className="home-badge">
          <span className="status-dot"></span>
          AI-POWERED HAND RECOGNITION
        </div>

        <h1>
          Play With Your
          <br />
          <span>Hands.</span>
        </h1>

        <p className="home-description">
          Experience Rock, Paper, Scissors like never before.
          Control the game with your hand gestures using
          real-time AI hand recognition.
        </p>

        <div className="gesture-preview">

          <div className="gesture-card">
            <span className="gesture-icon">✊</span>
            <span>ROCK</span>
          </div>

          <div className="gesture-card">
            <span className="gesture-icon">✋</span>
            <span>PAPER</span>
          </div>

          <div className="gesture-card">
            <span className="gesture-icon">✌️</span>
            <span>SCISSORS</span>
          </div>

        </div>

        <div className="home-actions">

          <button
            className="start-game-btn"
            onClick={handleStartGame}
          >
            Start Playing
            <span>→</span>
          </button>

          <button
            className="home-history-button"
            onClick={handleGameHistory}
          >
            Game History
          </button>

        </div>

        <p className="home-note">
          No keyboard. No controller. Just your hands.
        </p>

      </main>

      <footer className="home-footer">
        SMART HAND GESTURE GAME
        <span>•</span>
        POWERED BY AI
      </footer>

    </div>
  );
}

export default Home;
