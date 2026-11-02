
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Game.css";

const WS_URL = "ws://127.0.0.1:8000/api/v1/ws/gestures";

const gestureDetails = {
  Rock: {
    icon: "✊",
    description: "Rock"
  },
  Paper: {
    icon: "✋",
    description: "Paper"
  },
  Scissors: {
    icon: "✌️",
    description: "Scissors"
  }
};

function Game() {
  const navigate = useNavigate();

  const socketRef = useRef(null);
  const gameIdRef = useRef(null);

  const [connected, setConnected] = useState(false);

  const [round, setRound] = useState(0);
  const [playerScore, setPlayerScore] = useState(0);
  const [computerScore, setComputerScore] = useState(0);
  const [draws, setDraws] = useState(0);

  const [playerGesture, setPlayerGesture] = useState("Waiting...");
  const [computerGesture, setComputerGesture] = useState("Waiting...");
  const [roundResult, setRoundResult] = useState("Make your gesture");

  const [cameraFrame, setCameraFrame] = useState(null);
  const [gestureStable, setGestureStable] = useState(false);

  const [error, setError] = useState("");

  useEffect(() => {
    const socket = new WebSocket(WS_URL);
    socketRef.current = socket;

    socket.onopen = () => {
      setConnected(true);
      setError("");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "game_started") {
        gameIdRef.current = data.game_id;
      }

      if (
        data.type === "gesture_update" ||
        data.type === "game_completed"
      ) {
        // Live camera feed
        if (data.camera_frame) {
          setCameraFrame(
            `data:image/jpeg;base64,${data.camera_frame}`
          );
        }

        // Gesture recognition
        const stableHand = data.stable_gestures?.find(
          (hand) => hand.is_stable
        );

        if (stableHand) {
          setPlayerGesture(stableHand.stable_gesture);
          setGestureStable(true);
        } else {
          setGestureStable(false);
        }

        // Game result
        if (data.game_result) {
          const result = data.game_result;

          setRound(result.round);
          setPlayerScore(result.player_score);
          setComputerScore(result.computer_score);
          setDraws(result.draws);

          setPlayerGesture(result.player_choice);
          setComputerGesture(result.computer_choice);
          setRoundResult(result.round_result);

          if (result.game_completed) {
            socket.close();

            navigate("/result", {
              state: {
                gameId: gameIdRef.current,
                ...result
              }
            });
          }
        }
      }

      if (data.type === "error") {
        setError(data.message || "Something went wrong.");
      }
    };

    socket.onerror = () => {
      setError("Unable to connect to the game server.");
    };

    socket.onclose = () => {
      setConnected(false);
    };

    return () => {
      socket.close();
    };
  }, [navigate]);

  const handleExit = () => {
    if (socketRef.current) {
      socketRef.current.close();
    }

    navigate("/");
  };

  const getGestureIcon = (gesture) => {
    return gestureDetails[gesture]?.icon || "❔";
  };

  const getResultClass = () => {
    if (roundResult === "Player") return "result-win";
    if (roundResult === "Computer") return "result-lose";
    if (roundResult === "Draw") return "result-draw";

    return "result-default";
  };

  return (
    <div className="game-container">

      {/* Header */}
      <header className="game-header">

        <div className="game-brand">
          <span className="brand-icon">✊</span>
          <h2>Gesture<span>Play</span></h2>
        </div>

        <div className="connection-status">
          <span className={connected ? "online-dot" : "offline-dot"}></span>
          {connected ? "Connected" : "Connecting..."}
        </div>

        <button className="exit-button" onClick={handleExit}>
          Exit Game
        </button>

      </header>

      <main className="game-content">

        {/* Title */}
        <section className="game-title">
          <span className="game-label">AI POWERED GAMEPLAY</span>
          <h1>Rock Paper Scissors</h1>
          <p>Show your hand. Let AI recognize your move.</p>
        </section>

        {error && (
          <div className="game-error">
            {error}
          </div>
        )}

        {/* Camera */}
        <section className="camera-section">

          <div className="section-heading">
            <h2>Live Camera</h2>

            <span className={cameraFrame ? "live-badge" : "waiting-badge"}>
              <span className="live-dot"></span>
              {cameraFrame ? "LIVE" : "WAITING"}
            </span>
          </div>

          <div className="camera-display">
            {cameraFrame ? (
              <img
                src={cameraFrame}
                alt="Live hand gesture detection"
              />
            ) : (
              <div className="camera-placeholder">
                <span>📷</span>
                <p>Waiting for camera feed...</p>
              </div>
            )}
          </div>

          <div className="recognition-status">
            <span className={gestureStable ? "recognition-dot active" : "recognition-dot"}></span>

            {gestureStable
              ? "Gesture successfully recognized"
              : "Show your hand and hold your gesture"}
          </div>

        </section>

        {/* Scoreboard */}
        <section className="scoreboard">

          <div className="score-card">
            <span className="score-label">PLAYER</span>
            <h2>{playerScore}</h2>
            <span className="score-caption">Your Score</span>
          </div>

          <div className="round-card">
            <span className="score-label">CURRENT ROUND</span>
            <h2>{round}<span> / 5</span></h2>
            <div className="round-progress">
              <div
                className="round-progress-fill"
                style={{ width: `${(round / 5) * 100}%` }}
              ></div>
            </div>
          </div>

          <div className="score-card">
            <span className="score-label">COMPUTER</span>
            <h2>{computerScore}</h2>
            <span className="score-caption">Computer Score</span>
          </div>

        </section>

        {/* Player vs Computer */}
        <section className="game-arena">

          <div className="player-panel">

            <span className="panel-label">YOU</span>
            <h3>Your Gesture</h3>

            <div className="gesture-icon-display">
              {getGestureIcon(playerGesture)}
            </div>

            <div className="gesture-name">
              {playerGesture}
            </div>

            <p>AI Hand Recognition</p>

          </div>

          <div className="versus-section">
            <div className="versus-line"></div>
            <span>VS</span>
            <div className="versus-line"></div>
          </div>

          <div className="player-panel computer-panel">

            <span className="panel-label">OPPONENT</span>
            <h3>Computer</h3>

            <div className="gesture-icon-display">
              {getGestureIcon(computerGesture)}
            </div>

            <div className="gesture-name">
              {computerGesture}
            </div>

            <p>Random Selection</p>

          </div>

        </section>

        {/* Round Result */}
        <section className={`round-result ${getResultClass()}`}>
          <span className="result-label">ROUND RESULT</span>
          <h2>{roundResult}</h2>
          <p>Total Draws: {draws}</p>
        </section>

        {/* Instructions */}
        <section className="game-instructions">
          <h3>How to Play</h3>

          <div className="instruction-items">
            <div>
              <span>✊</span>
              <p>Rock</p>
            </div>

            <div>
              <span>✋</span>
              <p>Paper</p>
            </div>

            <div>
              <span>✌️</span>
              <p>Scissors</p>
            </div>
          </div>

          <p className="instruction-note">
            Hold your hand gesture steady until AI recognizes it.
          </p>
        </section>

      </main>

      <footer className="game-footer">
        SMART HAND GESTURE GAME · POWERED BY AI
      </footer>

    </div>
  );
}

export default Game;
