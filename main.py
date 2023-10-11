import sys
import database
from PyQt5 import QtWidgets
from ui import Ui_MainWindow
from ui_function import *
from utils import *


def initialize_ui_function(ui):
    combo_box_Initialize(ui)
    connect_ui_with_event(ui)


def connect_ui_with_event(ui):
    # tab 1
    ui.edgeSearchButton.clicked.connect(lambda: search_event(ui, 'edge'))
    ui.childSearchButton.clicked.connect(lambda: search_event(ui, 'child'))
    ui.addGroupButton.clicked.connect(lambda: add_group_event(ui))

    ui.edgeComboBox.currentIndexChanged.connect(
        lambda _: edge_combo_changed_event(ui))

    ui.bomComboBox.currentIndexChanged.connect(
        lambda _: bom_combobox_changed_event(ui))
    bom_combobox_changed_event(ui)

    ui.bomRefreshButton.clicked.connect(
        lambda _: refresh_bom_event(ui))

    # tab 2
    ui.deleteRowButton.clicked.connect(
        lambda: delete_selected_row(ui.bomTableView))
    ui.addProfileButton.clicked.connect(
        lambda: add_profile_event(ui))
    ui.addBomButton.clicked.connect(
        lambda: add_bom_event(ui))
    ui.clearBomButton.clicked.connect(
        lambda: clear_group_event(ui))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    MainWindow = QtWidgets.QMainWindow()
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
