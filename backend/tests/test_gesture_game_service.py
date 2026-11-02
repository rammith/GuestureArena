
import pytest

from app.services.gesture_game_service import GestureGameService


@pytest.fixture
def gesture_game():

    return GestureGameService()


def test_create_game_session(gesture_game):

    session = gesture_game.create_session(total_rounds=5)

    assert "game_id" in session
    assert session["total_rounds"] == 5
    assert session["message"] == "Game created successfully"


def test_play_valid_gesture(gesture_game):

    session = gesture_game.create_session(total_rounds=5)

    result = gesture_game.play_gesture(
        session["game_id"],
        "Rock"
    )

    assert result["player_choice"] == "Rock"
    assert result["computer_choice"] in [
        "Rock", "Paper", "Scissors"
    ]
    assert result["round"] == 1
    assert result["player_score"] >= 0
    assert result["computer_score"] >= 0
    assert result["game_completed"] is False


def test_invalid_gesture(gesture_game):

    session = gesture_game.create_session(total_rounds=5)

    with pytest.raises(ValueError, match="Invalid gesture"):

        gesture_game.play_gesture(
            session["game_id"],
            "Invalid"
        )


def test_score_updates(gesture_game):

    session = gesture_game.create_session(total_rounds=5)

    # Play multiple rounds
    for gesture in ["Rock", "Paper", "Scissors"]:

        result = gesture_game.play_gesture(
            session["game_id"],
            gesture
        )

    assert result["round"] == 3

    assert (
        result["player_score"]
        + result["computer_score"]
        + result["draws"]
    ) == 3


def test_game_completion(gesture_game):

    session = gesture_game.create_session(total_rounds=2)

    gesture_game.play_gesture(
        session["game_id"],
        "Rock"
    )

    result = gesture_game.play_gesture(
        session["game_id"],
        "Paper"
    )

    assert result["round"] == 2
    assert result["game_completed"] is True
    assert result["match_result"] in [
        "Player Wins",
        "Computer Wins",
        "Match Draw"
    ]


def test_cannot_play_after_game_completion(gesture_game):

    session = gesture_game.create_session(total_rounds=1)

    gesture_game.play_gesture(
        session["game_id"],
        "Rock"
    )

    with pytest.raises(RuntimeError, match="Game is already completed"):

        gesture_game.play_gesture(
            session["game_id"],
            "Paper"
        )
