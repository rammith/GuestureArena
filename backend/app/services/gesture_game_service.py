
from app.services.game_service import game_service


class GestureGameService:

    def __init__(self):

        self.game_service = game_service

    def create_session(self, total_rounds=5):

        session = self.game_service.create_game(total_rounds)

        return {
            "game_id": session["game_id"],
            "total_rounds": session["total_rounds"],
            "message": session["message"]
        }

    def play_gesture(self, game_id, gesture):

        if gesture not in ["Rock", "Paper", "Scissors"]:
            raise ValueError("Invalid gesture")

        # Play one round using the existing GameService
        round_result = self.game_service.play_round(
            game_id,
            gesture
        )

        # Get the latest game status
        game_status = self.game_service.get_game_status(
            game_id
        )

        return {
            "game_id": game_id,
            "round": round_result["round"],
            "player_choice": round_result["player_choice"],
            "computer_choice": round_result["computer_choice"],
            "round_result": round_result["result"],
            "player_score": round_result["player_score"],
            "computer_score": round_result["computer_score"],
            "draws": round_result["draws"],
            "game_completed": round_result["game_completed"],
            "match_result": game_status["match_result"]
        }


gesture_game_service = GestureGameService()
