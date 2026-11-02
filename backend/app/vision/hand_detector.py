
import cv2
import mediapipe as mp
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandDetector:

    def __init__(
        self,
        model_path="ml_models/hand_landmarker.task",
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_presence_confidence=0.5,
        min_tracking_confidence=0.5
    ):

        self.model_path = model_path
        self.max_num_hands = max_num_hands

        # Configure MediaPipe model
        base_options = python.BaseOptions(
            model_asset_path=self.model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=self.max_num_hands,
            min_hand_detection_confidence=min_detection_confidence,
            min_hand_presence_confidence=min_presence_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

        # Initialize hand detector
        self.detector = vision.HandLandmarker.create_from_options(
            options
        )

        self.previous_timestamp = 0

    def detect_hands(self, frame):

        if frame is None:
            raise ValueError("Invalid image frame")

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Convert OpenCV image to MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Generate timestamp in milliseconds
        timestamp = int(time.monotonic() * 1000)

        # Ensure timestamps are strictly increasing
        timestamp = max(
            timestamp,
            self.previous_timestamp + 1
        )

        self.previous_timestamp = timestamp

        # Detect hands
        results = self.detector.detect_for_video(
            mp_image,
            timestamp
        )

        # Draw detected landmarks
        if results.hand_landmarks:

            for hand_landmarks in results.hand_landmarks:

                height, width, _ = frame.shape

                points = []

                for landmark in hand_landmarks:

                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    points.append((x, y))

                    cv2.circle(
                        frame,
                        (x, y),
                        5,
                        (0, 255, 0),
                        -1
                    )

                # Draw connections between landmarks
                for start_idx, end_idx in HAND_CONNECTIONS:

                    cv2.line(
                        frame,
                        points[start_idx],
                        points[end_idx],
                        (255, 0, 0),
                        2
                    )

        return frame, results

    def close(self):

        self.detector.close()


# MediaPipe hand landmark connections
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]
