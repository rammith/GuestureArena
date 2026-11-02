
from typing import Literal

from pydantic import BaseModel, Field


class CreateGameRequest(BaseModel):

    total_rounds: int = Field(
        default=5,
        ge=1,
        le=20
    )


class PlayRoundRequest(BaseModel):

    player_choice: Literal["Rock", "Paper", "Scissors"]


class GameCreateResponse(BaseModel):

    game_id: str
    total_rounds: int
    message: str


class GameRoundResponse(BaseModel):

    round: int
    player_choice: str
    computer_choice: str
    result: str
    player_score: int
    computer_score: int
    draws: int
    game_completed: bool


class GameStatusResponse(BaseModel):

    game_id: str
    current_round: int
    total_rounds: int
    player_score: int
    computer_score: int
    draws: int
    match_result: str
    game_completed: bool
