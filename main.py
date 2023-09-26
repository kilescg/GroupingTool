import sys
from PyQt5 import QtWidgets
from custom_main_window import MyMainWindow
from ui import Ui_MainWindow
from ui_function_initialize import *

def initialize_ui_function(ui):
    combo_box_Initialize(ui)
    connect_ui_with_event(ui)

def connect_ui_with_event(ui):
    ui.reloadButton.clicked.connect(lambda : reload_camera_list_event(ui))
    ui.selectCameraButton.clicked.connect(lambda : select_camera_evenet(ui))

def combo_box_Initialize(ui):
    reload_camera_list_event(ui);

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    MainWindow = MyMainWindow(ui, lambda : camera_handler.update_camera_function(ui))
    ui.setupUi(MainWindow)
    '''
    USER SETUP BEGIN
    '''
    initialize_ui_function(ui)
    '''
    USER SETUP END
    '''
    MainWindow.show()
    sys.exit(app.exec_())
