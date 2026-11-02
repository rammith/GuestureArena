from uuid import uuid4

from app.game_engine.game_manager import GameManager
from app.repositories.game_repository import game_repository


class GameService:

    def __init__(self):
        self.games = {}

    def create_game(self, total_rounds):

        game_id = str(uuid4())

        game_manager = GameManager(
            total_rounds=total_rounds
        )

        # Save the initial game document in MongoDB
        game_repository.create_game(
            game_id,
            total_rounds
        )

        # Keep the active game in memory
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

        # Execute the existing game logic
        round_result = game.play_round(player_choice)

        # Get the updated game status
        game_status = self.get_game_status(game_id)

        # Persist the round and updated scores in MongoDB
        update_result = game_repository.add_round(
            game_id,
            round_result,
            game_status
        )

        if update_result.matched_count == 0:
            raise RuntimeError(
                "Game session not found in MongoDB"
            )

        return round_result

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

    def abandon_game(self, game_id):

        game = self.games.get(game_id)

        if game is None:
            return False

    # Do not abandon an already completed game
        if game.current_round >= game.total_rounds:
            return False

        result = game_repository.mark_game_abandoned(game_id)

    # Remove the inactive game from memory
        self.games.pop(game_id, None)

        return result.modified_count > 0

    

    def get_game_history(self, game_id):

        game = game_repository.get_game(game_id)

        if game is None:
            raise ValueError("Game not found")

        return game

    def get_all_game_history(self):

        return game_repository.get_all_games()


game_service = GameService()