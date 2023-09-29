from database import SDE_SQLLite
import os
import json


def add_device_event(ui):
    json_file = open("configuration.json")
    combo_box_json = json.load(json_file)
    child_mac_id = ui.childMacResult.text()
    device_type = ui.deviceTypeComboBox.currentText()
    device_name = ui.deviceNameComboBox.currentText()
    location = ui.locationComboBox.currentText()
    controller_type = ui.controllerTypeComboBox.currentText()
    device_type_index = combo_box_json["device_name_to_index"][device_name]
    child_mac_id = f"{device_type_index}_{child_mac_id}"

    json_file.close()


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
    pass


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
