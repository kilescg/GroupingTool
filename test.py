import cv2

def list_available_cameras():
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

if __name__ == "__main__":
    cameras = list_available_cameras()
    if cameras:
        print("Available cameras:")
        for camera in cameras:
            print(camera)
    else:
        print("No cameras found.")