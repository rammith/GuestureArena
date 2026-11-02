
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/Result.css";

function Result() {
  const navigate = useNavigate();
  const location = useLocation();

  const result = location.state;

  // Handle direct access without game results
  if (!result) {
    return (
      <div className="result-container">
        <div className="result-card">
          <h1>No Game Results Found</h1>
          <p>Complete a game to view your results.</p>

          <button
            className="play-again-btn"
            onClick={() => navigate("/")}
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  const {
    player_score,
    computer_score,
    draws,
    match_result,
    player_choice,
    computer_choice,
    round_result
  } = result;

  const isPlayerWinner = match_result === "Player Wins";
  const isComputerWinner = match_result === "Computer Wins";
  const isDraw = match_result === "Match Draw";

  const winnerTitle = isPlayerWinner
    ? "Congratulations!"
    : isComputerWinner
      ? "Computer Wins!"
      : "It's a Draw!";

  const winnerIcon = isPlayerWinner
    ? "🏆"
    : isComputerWinner
      ? "🤖"
      : "🤝";

  const handlePlayAgain = () => {
    navigate("/game");
  };

  const handleHome = () => {
    navigate("/");
  };

  return (
    <div className="result-container">

      {/* Header */}
      <header className="result-header">
        <h2>
          Gesture<span>Play</span>
        </h2>

        <span className="completed-badge">
          GAME COMPLETED
        </span>
      </header>

      <main className="result-content">

        {/* Winner Section */}
        <section className="winner-section">

          <div className="winner-icon">
            {winnerIcon}
          </div>

          <span className="result-subtitle">
            MATCH SUMMARY
          </span>

          <h1
            className={
              isPlayerWinner
                ? "winner-title player-winner"
                : isComputerWinner
                  ? "winner-title computer-winner"
                  : "winner-title draw-winner"
            }
          >
            {winnerTitle}
          </h1>

          <p className="winner-description">
            {isPlayerWinner
              ? "You played brilliantly and won the match!"
              : isComputerWinner
                ? "The computer won this time. Better luck next time!"
                : "Both players finished with the same score!"}
          </p>

        </section>

        {/* Final Score */}
        <section className="final-score-section">

          <div className="final-score-card">
            <span className="final-score-label">PLAYER</span>
            <h2>{player_score}</h2>
            <span className="final-score-caption">Your Score</span>
          </div>

          <div className="final-score-divider">
            VS
          </div>

          <div className="final-score-card">
            <span className="final-score-label">COMPUTER</span>
            <h2>{computer_score}</h2>
            <span className="final-score-caption">Computer Score</span>
          </div>

        </section>

        {/* Match Statistics */}
        <section className="match-statistics">

          <div className="stat-card">
            <span className="stat-icon">🎮</span>
            <h3>5</h3>
            <p>Total Rounds</p>
          </div>

          <div className="stat-card">
            <span className="stat-icon">🏆</span>
            <h3>{player_score}</h3>
            <p>Player Wins</p>
          </div>

          <div className="stat-card">
            <span className="stat-icon">🤖</span>
            <h3>{computer_score}</h3>
            <p>Computer Wins</p>
          </div>

          <div className="stat-card">
            <span className="stat-icon">🤝</span>
            <h3>{draws}</h3>
            <p>Draws</p>
          </div>

        </section>

        {/* Last Round Details */}
        <section className="last-round-section">

          <h2>Final Round Details</h2>

          <div className="last-round-details">

            <div>
              <span>Your Gesture</span>
              <h3>{player_choice}</h3>
            </div>

            <span className="round-vs">VS</span>

            <div>
              <span>Computer Gesture</span>
              <h3>{computer_choice}</h3>
            </div>

          </div>

          <div className="last-round-result">
            Final Round Result: <strong>{round_result}</strong>
          </div>

        </section>

        {/* Actions */}
        <section className="result-actions">

          <button
            className="play-again-btn"
            onClick={handlePlayAgain}
          >
            Play Again <span>↻</span>
          </button>

          <button
            className="home-btn"
            onClick={handleHome}
          >
            Back to Home
          </button>

        </section>

      </main>

      <footer className="result-footer">
        SMART HAND GESTURE GAME · POWERED BY AI
      </footer>

    </div>
  );
}

export default Result;
