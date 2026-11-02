
import cv2
import base64

from app.vision.camera import Camera
from app.vision.hand_detector import HandDetector
from app.vision.landmark_processor import LandmarkProcessor
from app.vision.finger_tracker import FingerTracker
from app.vision.gesture_classifier import GestureClassifier
from app.vision.gesture_stabilizer import GestureStabilizer


class VisionService:

    def __init__(self):

        self.camera = Camera()
        self.detector = None

        self.processor = LandmarkProcessor()
        self.tracker = FingerTracker()
        self.classifier = GestureClassifier()
        self.stabilizer = GestureStabilizer(stable_frames=8)

        self.is_running = False

    def start(self):

        if self.is_running:
            return

        self.detector = HandDetector()

        try:
            self.camera.start()
            self.stabilizer.reset()
            self.is_running = True

        except Exception:
            self.detector.close()
            self.detector = None
            raise

    def process_frame(self):

        if not self.is_running:
            raise RuntimeError("Camera is not running")

        frame = self.camera.read_frame()

        frame, results = self.detector.detect_hands(frame)

        hands_data = self.processor.process(
            results,
            frame.shape
        )

        finger_data = self.tracker.track(hands_data)

        gestures = self.classifier.classify(finger_data)

        stable_gestures = self.stabilizer.process(gestures)

        # Convert camera frame into JPEG
        success, buffer = cv2.imencode(
            ".jpg",
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 75]
        )

        if not success:
            raise RuntimeError("Unable to encode camera frame")

        # Encode JPEG image into Base64
        camera_frame = base64.b64encode(
            buffer
        ).decode("utf-8")

        return {
            "hands_detected": len(hands_data),
            "finger_states": finger_data,
            "gestures": gestures,
            "stable_gestures": stable_gestures,
            "camera_frame": camera_frame
        }

    def stop(self):

        if self.detector is not None:
            self.detector.close()
            self.detector = None

        self.camera.release()
        self.stabilizer.reset()
        self.is_running = False
