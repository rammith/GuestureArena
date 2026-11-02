from datetime import datetime, timezone
from app.core.database import database
from app.models.game_model import GameModel


class GameRepository:

    def __init__(self):
        self.collection = database["game_sessions"]

    def create_game(self, game_id, total_rounds):

        game_document = GameModel.create_game_document(
            game_id,
            total_rounds
        )

        self.collection.insert_one(game_document)

        return game_document

    def add_round(self, game_id, round_result, game_status):

        round_document = GameModel.create_round_document(
            round_result
        )

        update_data = {
            "current_round": game_status["current_round"],
            "player_score": game_status["player_score"],
            "computer_score": game_status["computer_score"],
            "draws": game_status["draws"],
            "match_result": game_status["match_result"],
            "status": (
                "completed"
                if game_status["game_completed"]
                else "in_progress"
            )
        }

        if game_status["game_completed"]:
            update_data["completed_at"] = datetime.now(timezone.utc)

        return self.collection.update_one(
            {"game_id": game_id},
            {
                "$push": {"rounds": round_document},
                "$set": update_data
            }
        )

    def mark_game_abandoned(self, game_id):

        return self.collection.update_one(
        {
            "game_id": game_id,
            "status": "in_progress"
        },
        {
            "$set": {
                "status": "abandoned",
                "match_result": "Game Abandoned",
                "completed_at": datetime.now(timezone.utc)
            }
        }
    )

    def get_game(self, game_id):

        return self.collection.find_one(
            {"game_id": game_id},
            {"_id": 0}
        )

    def get_all_games(self):

        return list(
            self.collection.find(
                {},
                {"_id": 0}
            ).sort("created_at", -1)
        )


game_repository = GameRepository()