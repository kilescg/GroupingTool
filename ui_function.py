from database import SDE_SQLLite
from PyQt5.QtWidgets import QMessageBox
from utils import *


def combo_box_Initialize(ui):
    sql_db = SDE_SQLLite('database/DB_sdeautodeploy.db')
    options = sql_db.select_data('bom', ['bom_id'])
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
        data_list = sql_db.search_value('child_device', 'child_id', keyword)
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


def bom_combobox_changed_event(ui):
    processed_config_list = []
    header = ['device_name_prefix', 'device_type',
              'controller_type', 'location', 'room']
    sql_db = SDE_SQLLite('database/DB_sdeautodeploy.db')
    value = ui.bomComboBox.currentText()
    query = f"""
            SELECT dp.name_prefix, dp.devicetype_id, dp.controllertype_id, dp.emplacement_id, dp.room
            FROM device_profile AS dp
            JOIN bom AS b ON dp.bom_id = b.bom_id
            WHERE b.bom_id= '{value}'
        """
    config_list = sql_db.execute_query(query)
    for config in config_list:
        device_name_prefix = config[0]
        device_type = sql_db.select_data(
            'device_type', ['devicetype_name'], f"devicetype_id={config[1]}")[0][0]
        controller_type = sql_db.select_data(
            'controller_type', ['controllertype_name'], f"controllertype_id={config[2]}")[0][0]
        location = sql_db.select_data(
            'emplacement_type', ['emplacement_name'], f"emplacement_id={config[3]}")[0][0]
        room = config[4]
        processed_config_list.append(
            [device_name_prefix, device_type, controller_type, location, room])
    populate_table(ui.groupListTableView, header, processed_config_list)


def refresh_bom_event(ui):
    ui.bomComboBox.clear()
    sql_db = SDE_SQLLite('database/DB_sdeautodeploy.db')
    box_id_list = sql_db.select_data('bom', ['bom_id'])
    for box_id in box_id_list:
        ui.bomComboBox.addItem(box_id[0])


def add_bom_event(ui):
    sql_db = SDE_SQLLite('database/DB_sdeautodeploy.db')
    headers = ['bom_id', 'name_prefix', 'devicetype_id',
               'controllertype_id', 'emplacement_id', 'room']
    bom_id = ui.bomNameLineEdit.text()
    if bom_id is None or bom_id in ('', []):
        QMessageBox.warning(
            None,
            "Warning",
            "Please fill the bom_id!",
            QMessageBox.Ok,
        )
        return
    data = get_data_from_table_view(ui.bomTableView)
    if data == []:
        QMessageBox.warning(
            None,
            "Warning",
            "Please fill the data!",
            QMessageBox.Ok,
        )
        return
    new_data = []
    for row in data:
        new_row = []
        new_row.append(row[0])
        new_row.append(sql_db.select_data('device_type', [
                       'devicetype_id'], f"devicetype_name='{row[1]}'")[0][0])
        new_row.append(sql_db.select_data('controller_type', [
                       'controllertype_id'], f"controllertype_name='{row[2]}'")[0][0])
        new_row.append(sql_db.select_data('emplacement_type', [
                       'emplacement_id'], f"emplacement_name='{row[3]}'")[0][0])
        new_row.append(row[4])
        new_data.append(new_row)
    sql_db.insert_data('bom', {'bom_id': bom_id})
    processed_data = [[bom_id] + sublist for sublist in new_data]
    for row in processed_data:
        sql_db.insert_data('device_profile', dict(zip(headers, row)))
    populate_table(ui.bomTableView, headers, [])


def add_profile_event(ui):
    headers = ['device_name_prefix', 'device_type',
               'controller_type', 'location', 'room']
    name_prefix = ui.macPrefixLineEdit.text()
    device_type = ui.deviceTypeComboBox.currentText()
    controller_type = ui.controllerTypeComboBox.currentText()
    location = ui.locationComboBox.currentText()
    room = ui.roomLineEdit.text()
    data = get_data_from_table_view(ui.bomTableView)
    new_profile = [name_prefix, device_type, controller_type,
                   location, room]
    if (name_prefix is not None and name_prefix not in ('', [])) and (room is not None and room not in ('', [])):
        if data == None:
            data = []
        data.append(new_profile)
        populate_table(ui.bomTableView, headers, data)
    else:
        QMessageBox.warning(
            None,
            "Warning",
            "All data must be selected!",
            QMessageBox.Ok,
        )
        return


def clear_group_event(ui):
    headers = ['device_name_prefix', 'device_type',
               'controller_type', 'location', 'room']
    populate_table(ui.bomTableView, headers, [])


def add_group_event(ui):
    sql_db = SDE_SQLLite('database/DB_sdeautodeploy.db')
    edge_id = ui.edgeComboBox.currentText()
    child_id = ui.childComboBox.currentText()
    bom_id = ui.bomComboBox.currentText()
    if edge_id == '' or child_id == '' or bom_id == '':
        ui.addStatusLabel.setText('<span style="color: red;">Fail!</span>')
        QMessageBox.warning(
            None,
            "Warning",
            "Please select all data!",
            QMessageBox.Ok,
        )
        return
    kitting_device = {
        'edge_id': edge_id,
        'child_id': child_id,
        'datetime': get_date_time()
    }
    sql_db.insert_data('kitting_device', kitting_device)
    updated_child = {
        'bom_id': bom_id
    }
    sql_db.update_data('child_device', updated_child, f"child_id='{child_id}'")
    ui.addStatusLabel.setText('<span style="color: green;">Success!</span>')


if __name__ == '__main__':
    search_val = 'Indoor'
    sql_db = SDE_SQLLite('database/DB_sdeautodeploy.db')
    print(sql_db.select_data('bom', ['bom_id']))
