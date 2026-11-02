
import json
import pytest
import websockets


@pytest.mark.asyncio
async def test_gesture_websocket():

    uri = "ws://127.0.0.1:8000/api/v1/ws/gestures"

    async with websockets.connect(uri) as websocket:

        print("Connected to gesture WebSocket")

        # Receive game started message
        response = await websocket.recv()
        data = json.loads(response)

        print("Game Started:", data)

        assert data["type"] == "game_started"
        assert "game_id" in data
        assert data["total_rounds"] == 5

        # Receive live gesture updates
        for _ in range(30):

            response = await websocket.recv()
            data = json.loads(response)

            print("WebSocket Update:", data)

            assert data["type"] in [
                "gesture_update",
                "game_completed"
            ]

            assert "hands_detected" in data
            assert "gestures" in data
            assert "stable_gestures" in data

            # Check game result when a new gesture is confirmed
            if data.get("game_result") is not None:

                print("Game Result:", data["game_result"])

            if data["type"] == "game_completed":
                break
