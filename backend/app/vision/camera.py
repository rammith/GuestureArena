
import cv2


class Camera:

    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None

    def start(self):
        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("Unable to access webcam")

        print("Camera started successfully!")

    def read_frame(self):
        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError("Camera is not initialized")

        success, frame = self.cap.read()

        if not success:
            raise RuntimeError("Unable to capture frame")

        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
            cv2.destroyAllWindows()
            print("Camera released successfully!")
