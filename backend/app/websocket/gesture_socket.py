
import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.vision_service import VisionService
from app.services.gesture_game_service import gesture_game_service


router = APIRouter()

camera_lock = asyncio.Lock()


@router.websocket("/ws/gestures")
async def gesture_websocket(websocket: WebSocket):

    await websocket.accept()

    if camera_lock.locked():
        await websocket.send_json({
            "error": "Camera is already being used"
        })
        await websocket.close(code=1013)
        return

    await camera_lock.acquire()

    vision_service = VisionService()
    game_id = None

    try:

        # Create a new game session
        session = gesture_game_service.create_session(
            total_rounds=5
        )

        game_id = session["game_id"]

        await websocket.send_json({
            "type": "game_started",
            **session
        })

        # Start camera
        await asyncio.to_thread(vision_service.start)

        while True:

            gesture_data = await asyncio.to_thread(
                vision_service.process_frame
            )

            stable_gestures = gesture_data["stable_gestures"]

            response = {
                "type": "gesture_update",
                "hands_detected": gesture_data["hands_detected"],
                "gestures": gesture_data["gestures"],
                "stable_gestures": stable_gestures,
                "camera_frame": gesture_data["camera_frame"],
                "game_result": None
            }

            # Check for newly confirmed gestures
            for hand in stable_gestures:

                if hand["is_new"]:

                    game_result = gesture_game_service.play_gesture(
                        game_id,
                        hand["stable_gesture"]
                    )

                    response["game_result"] = game_result

                    if game_result["game_completed"]:
                        response["type"] = "game_completed"

                    break

            # Send camera frame and gesture information
            await websocket.send_json(response)

            if response["type"] == "game_completed":
                break

            await asyncio.sleep(0.03)

    except WebSocketDisconnect:

        print("WebSocket client disconnected")

    except Exception as error:

        print(f"Gesture WebSocket error: {error}")

        try:
            await websocket.send_json({
                "type": "error",
                "message": str(error)
            })
        except Exception:
            pass

    finally:

        # Mark unfinished games as abandoned
        if game_id is not None:
            try:
                await asyncio.to_thread(
                    gesture_game_service.abandon_session,
                    game_id
                )
            except Exception as error:
                print(f"Unable to update game status: {error}")

        await asyncio.to_thread(vision_service.stop)
        camera_lock.release()
