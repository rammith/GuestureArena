
class GestureStabilizer:

    def __init__(self, stable_frames=8):

        self.stable_frames = stable_frames
        self.hand_states = {}

        self.valid_gestures = ["Rock", "Paper", "Scissors"]

    def process(self, gestures):

        results = []
        detected_hand_ids = set()

        for hand in gestures:

            hand_index = hand["hand_index"]
            handedness = hand["handedness"]
            gesture = hand["gesture"]

            detected_hand_ids.add(hand_index)

            # Initialize state for a newly detected hand
            if hand_index not in self.hand_states:

                self.hand_states[hand_index] = {
                    "candidate": None,
                    "count": 0,
                    "active_gesture": None
                }

            state = self.hand_states[hand_index]

            is_new = False

            if gesture in self.valid_gestures:

                # Count consecutive frames of the same gesture
                if state["candidate"] == gesture:
                    state["count"] += 1

                else:
                    state["candidate"] = gesture
                    state["count"] = 1

                # Confirm gesture after enough consecutive frames
                if state["count"] >= self.stable_frames:

                    if state["active_gesture"] != gesture:

                        state["active_gesture"] = gesture
                        is_new = True

            else:
                # Reset candidate when gesture is unknown
                state["candidate"] = None
                state["count"] = 0

            results.append({
                "hand_index": hand_index,
                "handedness": handedness,
                "detected_gesture": gesture,
                "stable_gesture": state["active_gesture"],
                "is_stable": (
                    gesture == state["active_gesture"]
                    and state["count"] >= self.stable_frames
                ),
                "is_new": is_new
            })

        # Remove states for hands that are no longer detected
        missing_hands = set(self.hand_states.keys()) - detected_hand_ids

        for hand_index in missing_hands:
            del self.hand_states[hand_index]

        return results

    def reset(self):

        self.hand_states.clear()
