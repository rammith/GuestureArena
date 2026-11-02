from fastapi import APIRouter, HTTPException

from app.services.game_service import game_service


router = APIRouter()


@router.get("/history")
def get_all_game_history():

    try:
        games = game_service.get_all_game_history()

        return {
            "status": "success",
            "total_games": len(games),
            "games": games
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve game history: {str(error)}"
        )


@router.get("/history/{game_id}")
def get_game_history(game_id: str):

    try:
        game = game_service.get_game_history(game_id)

        return {
            "status": "success",
            "game": game
        }

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve game: {str(error)}"
        )