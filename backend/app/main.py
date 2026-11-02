from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.core.database import (
    check_database_connection,
    close_database_connection
)

from app.api.routes import health, game, history
from app.websocket import gesture_socket

from fastapi.middleware.cors import CORSMiddleware





@asynccontextmanager
async def lifespan(app: FastAPI):

    # Application startup
    print("Starting Smart Hand Gesture Game API...")

    if not check_database_connection():
        raise RuntimeError("MongoDB connection failed")

    print("Application started successfully!")

    yield

    # Application shutdown
    print("Shutting down application...")
    close_database_connection()
    print("MongoDB connection closed.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

app.include_router(
    history.router,
    prefix=settings.API_PREFIX,
    tags=["Game History"]
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Smart Hand Gesture Game API"
    }