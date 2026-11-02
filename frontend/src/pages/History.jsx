import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/History.css";

const API_URL = "http://127.0.0.1:8000/api/v1";

function History() {
  const navigate = useNavigate();

  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedGame, setSelectedGame] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch(`${API_URL}/history`);

        if (!response.ok) {
          throw new Error("Unable to retrieve game history");
        }

        const data = await response.json();
        setGames(data.games || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const playerWins = games.filter(
    (game) => game.match_result === "Player Wins"
  ).length;

  const computerWins = games.filter(
    (game) => game.match_result === "Computer Wins"
  ).length;

  const draws = games.filter(
    (game) => game.match_result === "Match Draw"
  ).length;

  const formatDate = (date) => {
    if (!date) return "N/A";

    return new Date(date).toLocaleString();
  };

  const getResultClass = (result) => {
    if (result === "Player Wins") return "history-win";
    if (result === "Computer Wins") return "history-lose";
    if (result === "Game Abandoned") return "history-abandoned";
    return "history-draw";
  };

  return (
    <div className="history-container">

      <header className="history-header">
        <div className="history-brand">
          <span>✊</span>
          <h2>Gesture<span>Play</span></h2>
        </div>

        <button
          className="history-back-button"
          onClick={() => navigate("/")}
        >
          Back Home
        </button>
      </header>

      <main className="history-content">

        <section className="history-title">
          <span className="history-label">YOUR GAME RECORDS</span>
          <h1>Game History</h1>
          <p>Review your previous matches and performance.</p>
        </section>

        {loading && (
          <p className="history-message">Loading game history...</p>
        )}

        {error && (
          <p className="history-error">{error}</p>
        )}

        {!loading && !error && (
          <>
            <section className="history-stats">

              <div className="history-stat-card">
                <span>Total Games</span>
                <h2>{games.length}</h2>
              </div>

              <div className="history-stat-card">
                <span>Player Wins</span>
                <h2>{playerWins}</h2>
              </div>

              <div className="history-stat-card">
                <span>Computer Wins</span>
                <h2>{computerWins}</h2>
              </div>

              <div className="history-stat-card">
                <span>Draws</span>
                <h2>{draws}</h2>
              </div>

            </section>

            <section className="history-list-section">
              <h2>Previous Matches</h2>

              {games.length === 0 ? (
                <div className="history-empty">
                  <span>🎮</span>
                  <h3>No Games Played Yet</h3>
                  <p>Start playing to build your game history.</p>
                  <button onClick={() => navigate("/game")}>
                    Start Playing
                  </button>
                </div>
              ) : (
                <div className="history-table-wrapper">
                  <table className="history-table">
                    <thead>
                      <tr>
                        <th>Game ID</th>
                        <th>Date</th>
                        <th>Player Score</th>
                        <th>Computer Score</th>
                        <th>Result</th>
                        <th>Action</th>
                      </tr>
                    </thead>

                    <tbody>
                      {games.map((game) => (
                        <tr key={game.game_id}>
                          <td>
                            {game.game_id.slice(0, 8)}...
                          </td>

                          <td>{formatDate(game.created_at)}</td>

                          <td>{game.player_score}</td>

                          <td>{game.computer_score}</td>

                          <td>
                            <span className={getResultClass(game.match_result)}>
                              {game.match_result}
                            </span>
                          </td>

                          <td>
                            <button
                              className="history-view-button"
                              onClick={() => setSelectedGame(game)}
                            >
                              View Details
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </section>

            {selectedGame && (
              <section className="history-details">

                <div className="history-details-header">
                  <h2>Match Details</h2>

                  <button
                    onClick={() => setSelectedGame(null)}
                  >
                    Close
                  </button>
                </div>

                <div className="history-details-summary">
                  <p>
                    **Match Result:** {selectedGame.match_result}
                  </p>
                  <p>
                    **Player Score:** {selectedGame.player_score}
                  </p>
                  <p>
                    **Computer Score:** {selectedGame.computer_score}
                  </p>
                  <p>
                    **Draws:** {selectedGame.draws}
                  </p>
                </div>

                <h3>Round-by-Round Results</h3>

                <div className="history-rounds">
                  {selectedGame.rounds.map((round) => (
                    <div
                      className="history-round-card"
                      key={round.round}
                    >
                      <h4>Round {round.round}</h4>

                      <p>Your Choice: {round.player_choice}</p>
                      <p>Computer Choice: {round.computer_choice}</p>
                      <p>Result: {round.result}</p>
                    </div>
                  ))}
                </div>

              </section>
            )}
          </>
        )}

      </main>
    </div>
  );
}

export default History;