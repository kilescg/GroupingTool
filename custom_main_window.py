import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self, ui, update_camera_function):
        super().__init__()
        self.ui = ui
        self.timer = QTimer(self)
        self.timer.timeout.connect(update_camera_function)
        self.timer.start(10)