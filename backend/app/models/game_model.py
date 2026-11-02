from datetime import datetime, timezone


class GameModel:

    @staticmethod
    def create_game_document(game_id, total_rounds):

        return {
            "game_id": game_id,
            "total_rounds": total_rounds,
            "current_round": 0,
            "player_score": 0,
            "computer_score": 0,
            "draws": 0,
            "match_result": "Game is still in progress",
            "status": "in_progress",
            "rounds": [],
            "created_at": datetime.now(timezone.utc),
            "completed_at": None
        }

    @staticmethod
    def create_round_document(round_result):

        return {
            "round": round_result["round"],
            "player_choice": round_result["player_choice"],
            "computer_choice": round_result["computer_choice"],
            "result": round_result["result"]
        }