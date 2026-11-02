
from fastapi import FastAPI

from app.core.config import settings
from app.api.routes import health, game

from app.websocket import gesture_socket


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)


app.include_router(
    health.router,
    prefix=settings.API_PREFIX,
    tags=["Health"]
)

app.include_router(
    game.router,
    prefix=settings.API_PREFIX,
    tags=["Game"]
)

app.include_router(
    gesture_socket.router,
    prefix=settings.API_PREFIX,
    tags=["WebSocket"]
)


@app.get("/")
def root():

    return {
        "message": "Welcome to Smart Hand Gesture Game API"
    }
