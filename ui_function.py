from database import SDE_SQLLite
from PyQt5.QtWidgets import QMessageBox
from utils import *


def combo_box_Initialize(ui):
    sql_db = SDE_SQLLite('database/DB_sdeautodeploy.db')
    options = sql_db.select_data('project', ['project_name'])
    for option in options:
        ui.bomComboBox.addItem(option[0])
    device_type = sql_db.select_data('device_type', ['devicetype_name'])
    for option in device_type:
        ui.deviceTypeComboBox.addItem(option[0])
    emplacement_type = sql_db.select_data(
        'emplacement_type', ['emplacement_name'])
    for option in emplacement_type:
        ui.locationComboBox.addItem(option[0])
    controller_type = sql_db.select_data(
        'controller_type', ['controllertype_name'])
    for option in controller_type:
        ui.controllerTypeComboBox.addItem(option[0])


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


def edge_combo_changed_event(ui):
    sql_db = SDE_SQLLite('database/DB_sdeautodeploy.db')
    query = """
            SELECT n.note_detail
            FROM edge_device AS e
            JOIN note AS n ON e.note_id = n.note_id
            WHERE e.edge_id = ?
        """
    value = ui.edgeComboBox.currentText().strip()
    if not value:
        return
    note = sql_db.execute_query(query, (value,))
    if len(note) != 0:
        note = note[0][0]
        ui.noteTextBrowser.setText(note)
    else:
        ui.noteTextBrowser.setText("")


def project_combo_changed_event(ui):
    processed_config_list = []
    header = ['device_name_prefix', 'device_type',
              'controller_type', 'location', 'room']
    sql_db = SDE_SQLLite('database/DB_sdeautodeploy.db')
    query = """
            SELECT dc.device_name_prefix, dc.devicetype_id, dc.controllertype_id, dc.emplacement_id, dc.room
            FROM device_configuration AS dc
            JOIN project AS p ON dc.project_id = p.project_id
            WHERE p.project_name = ?
        """
    value = ui.bomComboBox.currentText()
    config_list = sql_db.execute_query(query, (value,))
    for config in config_list:
        device_name_prefix = config[0]
        device_type = sql_db.select_data(
            'device_type', ['devicetype_name'], f"devicetype_id='{config[1]}'")[0][0]
        controller_type = sql_db.select_data(
            'controller_type', ['controllertype_name'], f"controllertype_id='{config[2]}'")[0][0]
        location = sql_db.select_data(
            'emplacement_type', ['emplacement_name'], f"emplacement_id='{config[3]}'")[0][0]
        room = config[4]
        processed_config_list.append(
            [device_name_prefix, device_type, controller_type, location, room])
    populate_table(ui.groupListTableView, header, processed_config_list)


def add_group_event(ui):
    pass


if __name__ == '__main__':
    project_combo_changed_event('fame')
