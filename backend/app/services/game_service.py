
from uuid import uuid4

from app.game_engine.game_manager import GameManager


class GameService:

    def __init__(self):

        self.games = {}

    def create_game(self, total_rounds):

        game_id = str(uuid4())

        game_manager = GameManager(
            total_rounds=total_rounds
        )

        self.games[game_id] = game_manager

        return {
            "game_id": game_id,
            "total_rounds": total_rounds,
            "message": "Game created successfully"
        }

    def play_round(self, game_id, player_choice):

        game = self.games.get(game_id)

        if game is None:
            raise ValueError("Game not found")

        return game.play_round(player_choice)

    def get_game_status(self, game_id):

        game = self.games.get(game_id)

        if game is None:
            raise ValueError("Game not found")

        return {
            "game_id": game_id,
            "current_round": game.current_round,
            "total_rounds": game.total_rounds,
            "player_score": game.player_score,
            "computer_score": game.computer_score,
            "draws": game.draws,
            "match_result": game.get_match_result(),
            "game_completed": (
                game.current_round == game.total_rounds
            )
        }


game_service = GameService()
