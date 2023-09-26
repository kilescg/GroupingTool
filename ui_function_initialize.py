from camera import Camera

camera_handler = Camera()

def reload_camera_list_event(ui):
    camera_list = camera_handler.list_available_camera()
    ui.cameraListComboBox.clear()
    for camera in camera_list:
        ui.cameraListComboBox.addItem(camera)

def select_camera_evenet(ui):
    target_camera = int(ui.cameraListComboBox.currentText().strip().split(" ")[1])
    camera_handler.initailize_video_capture(target_camera)