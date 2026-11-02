
from app.game_engine.game_rules import GameRules


def test_player_wins():

    game = GameRules()

    assert game.determine_winner("Rock", "Scissors") == "Player"


def test_computer_wins():

    game = GameRules()

    assert game.determine_winner("Rock", "Paper") == "Computer"


def test_draw():

    game = GameRules()

    assert game.determine_winner("Rock", "Rock") == "Draw"
