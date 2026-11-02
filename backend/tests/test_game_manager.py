
from app.game_engine.game_manager import GameManager


def test_player_score_updates():

    game = GameManager(total_rounds=3)

    game.game_rules.get_computer_choice = lambda: "Scissors"

    result = game.play_round("Rock")

    assert result["result"] == "Player"
    assert result["player_score"] == 1
    assert result["computer_score"] == 0


def test_computer_score_updates():

    game = GameManager(total_rounds=3)

    game.game_rules.get_computer_choice = lambda: "Paper"

    result = game.play_round("Rock")

    assert result["result"] == "Computer"
    assert result["computer_score"] == 1


def test_draw_updates():

    game = GameManager(total_rounds=3)

    game.game_rules.get_computer_choice = lambda: "Rock"

    result = game.play_round("Rock")

    assert result["result"] == "Draw"
    assert result["draws"] == 1



def test_match_result():

    game = GameManager(total_rounds=2)

    computer_choices = iter(["Scissors", "Rock"])

    game.game_rules.get_computer_choice = lambda: next(computer_choices)

    game.play_round("Rock")
    game.play_round("Paper")

    assert game.get_match_result() == "Player Wins"


def test_game_completion():

    game = GameManager(total_rounds=1)

    game.game_rules.get_computer_choice = lambda: "Rock"

    result = game.play_round("Paper")

    assert result["game_completed"] is True


def test_cannot_play_after_completion():

    game = GameManager(total_rounds=1)

    game.game_rules.get_computer_choice = lambda: "Rock"

    game.play_round("Paper")

    try:
        game.play_round("Rock")
        assert False, "Expected RuntimeError"
    except RuntimeError:
        assert True
