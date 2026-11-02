
# import math


# class FingerTracker:

#     def __init__(self):
#         self.finger_points = {
#             "thumb": (4, 3),
#             "index": (8, 6),
#             "middle": (12, 10),
#             "ring": (16, 14),
#             "pinky": (20, 18)
#         }

#     def _distance(self, point1, point2):

#         return math.hypot(
#             point1["normalized_x"] - point2["normalized_x"],
#             point1["normalized_y"] - point2["normalized_y"]
#         )

#     def track(self, hands_data):

#         tracked_hands = []

#         for hand in hands_data:

#             landmarks = hand["landmarks"]
#             wrist = landmarks[0]

#             finger_states = {}

#             for finger, (tip_id, joint_id) in self.finger_points.items():

#                 tip = landmarks[tip_id]
#                 joint = landmarks[joint_id]

#                 tip_distance = self._distance(tip, wrist)
#                 joint_distance = self._distance(joint, wrist)

#                 finger_states[finger] = tip_distance > joint_distance

#             tracked_hands.append({
#                 "hand_index": hand["hand_index"],
#                 "handedness": hand["handedness"],
#                 "fingers": finger_states,
#                 "extended_count": sum(finger_states.values())
#             })

#         return tracked_hands



import math


class FingerTracker:

    def __init__(self):

        self.finger_points = {
            "index": (8, 6),
            "middle": (12, 10),
            "ring": (16, 14),
            "pinky": (20, 18)
        }

    def _distance(self, point1, point2):

        return math.hypot(
            point1["normalized_x"] - point2["normalized_x"],
            point1["normalized_y"] - point2["normalized_y"]
        )

    def track(self, hands_data):

        tracked_hands = []

        for hand in hands_data:

            landmarks = hand["landmarks"]

            wrist = landmarks[0]

            finger_states = {}

            # Track four fingers
            for finger, (tip_id, joint_id) in self.finger_points.items():

                tip = landmarks[tip_id]
                joint = landmarks[joint_id]

                tip_distance = self._distance(tip, wrist)
                joint_distance = self._distance(joint, wrist)

                finger_states[finger] = (
                    tip_distance > joint_distance
                )

            # Track thumb separately
            thumb_tip = landmarks[4]
            index_mcp = landmarks[5]
            pinky_mcp = landmarks[17]

            thumb_distance = self._distance(
                thumb_tip,
                index_mcp
            )

            palm_width = self._distance(
                index_mcp,
                pinky_mcp
            )

            finger_states["thumb"] = (
                thumb_distance > palm_width * 0.5
            )

            tracked_hands.append({
                "hand_index": hand["hand_index"],
                "handedness": hand["handedness"],
                "fingers": finger_states,
                "extended_count": sum(finger_states.values())
            })

        return tracked_hands
