
import random


class GameRules:

    CHOICES = ["Rock", "Paper", "Scissors"]

    def get_computer_choice(self):

        return random.choice(self.CHOICES)

    def determine_winner(self, player_choice, computer_choice):

        if player_choice not in self.CHOICES:
            raise ValueError("Invalid player choice")

        if computer_choice not in self.CHOICES:
            raise ValueError("Invalid computer choice")

        if player_choice == computer_choice:
            return "Draw"

        winning_combinations = {
            "Rock": "Scissors",
            "Paper": "Rock",
            "Scissors": "Paper"
        }

        if winning_combinations[player_choice] == computer_choice:
            return "Player"

        return "Computer"
