
from app.vision.gesture_stabilizer import GestureStabilizer


def create_gesture(gesture, hand_index=0):

    return {
        "hand_index": hand_index,
        "handedness": "Left",
        "gesture": gesture
    }


def test_gesture_not_stable_before_threshold():

    stabilizer = GestureStabilizer(stable_frames=8)

    for _ in range(7):

        result = stabilizer.process([
            create_gesture("Rock")
        ])

    assert result[0]["stable_gesture"] is None
    assert result[0]["is_stable"] is False
    assert result[0]["is_new"] is False


def test_gesture_becomes_stable_at_threshold():

    stabilizer = GestureStabilizer(stable_frames=8)

    for _ in range(8):

        result = stabilizer.process([
            create_gesture("Paper")
        ])

    assert result[0]["stable_gesture"] == "Paper"
    assert result[0]["is_stable"] is True
    assert result[0]["is_new"] is True


def test_same_gesture_does_not_trigger_twice():

    stabilizer = GestureStabilizer(stable_frames=8)

    for _ in range(8):
        stabilizer.process([create_gesture("Rock")])

    result = stabilizer.process([create_gesture("Rock")])

    assert result[0]["is_stable"] is True
    assert result[0]["is_new"] is False


def test_new_gesture_triggers_new_action():

    stabilizer = GestureStabilizer(stable_frames=8)

    for _ in range(8):
        stabilizer.process([create_gesture("Rock")])

    for _ in range(8):
        result = stabilizer.process([create_gesture("Scissors")])

    assert result[0]["stable_gesture"] == "Scissors"
    assert result[0]["is_new"] is True


def test_unknown_gesture_resets_candidate():

    stabilizer = GestureStabilizer(stable_frames=8)

    for _ in range(5):
        stabilizer.process([create_gesture("Paper")])

    result = stabilizer.process([create_gesture("Unknown")])

    assert result[0]["stable_gesture"] is None
    assert result[0]["is_stable"] is False


def test_reset_clears_hand_states():

    stabilizer = GestureStabilizer(stable_frames=8)

    for _ in range(8):
        stabilizer.process([create_gesture("Rock")])

    stabilizer.reset()

    result = stabilizer.process([create_gesture("Paper")])

    assert result[0]["stable_gesture"] is None
    assert result[0]["is_new"] is False
