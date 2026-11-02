
from fastapi import APIRouter, HTTPException, status

from app.schemas.game_schema import (
    CreateGameRequest,
    PlayRoundRequest,
    GameCreateResponse,
    GameRoundResponse,
    GameStatusResponse
)

from app.services.game_service import game_service


router = APIRouter()


@router.post(
    "/games",
    response_model=GameCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def create_game(request: CreateGameRequest):

    return game_service.create_game(
        request.total_rounds
    )


@router.post(
    "/games/{game_id}/round",
    response_model=GameRoundResponse
)
def play_round(game_id: str, request: PlayRoundRequest):

    try:

        return game_service.play_round(
            game_id,
            request.player_choice
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except RuntimeError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get(
    "/games/{game_id}",
    response_model=GameStatusResponse
)
def get_game_status(game_id: str):

    try:

        return game_service.get_game_status(game_id)

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
