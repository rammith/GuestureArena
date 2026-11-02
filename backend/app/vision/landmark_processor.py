
class LandmarkProcessor:

    def process(self, results, frame_shape):

        hands_data = []

        if not results.hand_landmarks:
            return hands_data

        height, width = frame_shape[:2]

        for hand_index, hand_landmarks in enumerate(
            results.hand_landmarks
        ):

            landmarks = []

            for landmark_id, landmark in enumerate(hand_landmarks):

                x = int(landmark.x * width)
                y = int(landmark.y * height)
                z = landmark.z

                landmarks.append({
                    "id": landmark_id,
                    "x": x,
                    "y": y,
                    "z": z,
                    "normalized_x": landmark.x,
                    "normalized_y": landmark.y
                })

            handedness = "Unknown"

            if results.handedness:
                handedness = results.handedness[hand_index][0].category_name

            hands_data.append({
                "hand_index": hand_index,
                "handedness": handedness,
                "landmarks": landmarks
            })

        return hands_data
