
import cv2

from app.vision.camera import Camera
from app.vision.hand_detector import HandDetector
from app.vision.landmark_processor import LandmarkProcessor
from app.vision.finger_tracker import FingerTracker
from app.vision.gesture_classifier import GestureClassifier


def main():

    camera = Camera()
    detector = HandDetector()
    processor = LandmarkProcessor()
    tracker = FingerTracker()
    classifier = GestureClassifier()

    try:

        camera.start()

        while True:

            frame = camera.read_frame()

            frame, results = detector.detect_hands(frame)

            hands_data = processor.process(
                results,
                frame.shape
            )

            finger_data = tracker.track(hands_data)

            gestures = classifier.classify(finger_data)

            display_frame = cv2.flip(frame, 1)

            for index, hand in enumerate(gestures):

                cv2.putText(
                    display_frame,
                    f"{hand['handedness']}: {hand['gesture']}",
                    (10, 70 + (index * 40)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            cv2.putText(
                display_frame,
                f"Hands Detected: {len(hands_data)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.imshow(
                "Smart Hand Gesture Game",
                display_frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("p"):
                print("\nDetected Gestures:")
                print(gestures)

            if key == ord("q"):
                break

    except (RuntimeError, ValueError) as error:

        print(f"Application Error: {error}")

    finally:

        detector.close()
        camera.release()


if __name__ == "__main__":
    main()
