from database import SDE_SQLLite
from PyQt5.QtWidgets import QMessageBox
from utils import *


def add_device_event(ui):
    headers = ["edge mac id", "child mac id", "device type",
               "controller type", "location", "datetime"]
    edge_mac_id = ui.edgeComboBox.currentText()
    mac_prefix = ui.macPrefixLineEdit.text()
    child_mac_id = mac_prefix + "_" + ui.childComboBox.currentText()
    device_type = ui.deviceTypeComboBox.currentText()
    controller_type = ui.controllerTypeComboBox.currentText()
    location = ui.locationComboBox.currentText()
    datetime = get_date_time()
    data = get_data_from_table_view(ui.groupListTableView)
    new_device = [edge_mac_id, child_mac_id, device_type,
                  controller_type, location, datetime]
    if all(item is not None and item not in ('', []) for item in new_device) and (mac_prefix is not None and mac_prefix not in ('', [])):
        if data == None:
            data = []
        data.append(new_device)
        populate_table(ui.groupListTableView, headers, data)
    else:
        QMessageBox.warning(
            None,
            "Warning",
            "All data must be selected!",
            QMessageBox.Ok,
        )
        return


def search_event(ui, item_type):
    sql_db = SDE_SQLLite('database/DB_sdeautodeploy.db')
    if item_type == 'edge':
        keyword = ui.edgeSearchLineEdit.text()
        data_list = sql_db.search_value('edge_device', 'edge_id', keyword)
        ui.edgeComboBox.clear()
        for option in data_list:
            ui.edgeComboBox.addItem(option[0])
    elif item_type == 'child':
        keyword = ui.childSearchLineEdit.text()
        data_list = sql_db.search_value('device_incoming', 'mac_id', keyword)
        ui.childComboBox.clear()
        for option in data_list:
            ui.childComboBox.addItem(option[0])


def clear_group_event(ui):
    headers = ["edge mac id", "child mac id", "device type",
               "controller type", "location", "datetime"]
    populate_table(ui.groupListTableView, headers, [])


def combo_box_Initialize(ui):
    sql_db = SDE_SQLLite('database/DB_sdeautodeploy.db')
    device_type = sql_db.select_from_table('device_type', ['devicetype_name'])
    for option in device_type:
        ui.deviceTypeComboBox.addItem(option['devicetype_name'])
    emplacement_type = sql_db.select_from_table(
        'emplacement_type', ['emplacement_name'])
    for option in emplacement_type:
        ui.locationComboBox.addItem(option['emplacement_name'])
    controller_type = sql_db.select_from_table(
        'controller_type', ['controllertype_name'])
    for option in controller_type:
        ui.controllerTypeComboBox.addItem(option['controllertype_name'])


def edge_combo_changed_event(ui):
    sql_db = SDE_SQLLite('database/DB_sdeautodeploy.db')
    note = sql_db.get_note_details_by_edge_id(ui.edgeComboBox.currentText())
    if len(note) != 0:
        note = "Note :" + note[0][0]
        ui.edgeNoteLabel.setText(note)
