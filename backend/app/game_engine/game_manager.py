
from app.game_engine.game_rules import GameRules


class GameManager:

    def __init__(self, total_rounds=5):

        self.game_rules = GameRules()
        self.total_rounds = total_rounds

        self.current_round = 0
        self.player_score = 0
        self.computer_score = 0
        self.draws = 0

    def play_round(self, player_choice):

        if self.current_round >= self.total_rounds:
            raise RuntimeError("Game is already completed")

        computer_choice = self.game_rules.get_computer_choice()

        result = self.game_rules.determine_winner(
            player_choice,
            computer_choice
        )

        self.current_round += 1

        if result == "Player":
            self.player_score += 1

        elif result == "Computer":
            self.computer_score += 1

        else:
            self.draws += 1

        return {
            "round": self.current_round,
            "player_choice": player_choice,
            "computer_choice": computer_choice,
            "result": result,
            "player_score": self.player_score,
            "computer_score": self.computer_score,
            "draws": self.draws,
            "game_completed": self.current_round == self.total_rounds
        }

    def get_match_result(self):

        if self.current_round < self.total_rounds:
            return "Game is still in progress"

        if self.player_score > self.computer_score:
            return "Player Wins"

        elif self.computer_score > self.player_score:
            return "Computer Wins"

        return "Match Draw"
