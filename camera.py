import cv2
from PyQt5.QtGui import QImage, QPixmap
from enum import Enum
 
class ScanMode(Enum):
    NONE = 0
    SCAN_EDGE_DEVICE = 1
    SCAN_CHILD_DEVICE = 2

class Camera:
    def __init__(self):
        self.camera = None
        self.current_image = None

    def list_available_camera(self):
        available_cameras = []
        index = 0

        while True:
            camera = cv2.VideoCapture(index)
            if not camera.isOpened():
                break
            else:
                available_cameras.append(f"Camera {index}")
                camera.release()
            index += 1

        return available_cameras
    
    def initailize_video_capture(self, index):
        if self.camera != None:
            if self.camera.isOpend():
                self.camera.release()
        self.camera = cv2.VideoCapture(index)

    def update_camera_function(self, ui):
        if self.camera != None:
            ret, frame = self.camera.read()  # Read a frame from the camera

            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.current_image = frame_rgb;

                # Convert the RGB image to a QImage
                height, width, channel = frame_rgb.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)

                # Convert QImage to QPixmap and display it on the label
                pixmap = QPixmap.fromImage(q_image)
                ui.liveCameraLabel.setPixmap(pixmap)

    def decode_qrcode(self):
        # Decode QR codes in the image
        qcd = cv2.QRCodeDetector()

        retval, decoded_info, _, _ = qcd.detectAndDecodeMulti(self.current_image)
        if retval:
            return decoded_info[0]
        else:
            return ''