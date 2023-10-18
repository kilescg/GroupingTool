from database import *
from PyQt5.QtWidgets import QMessageBox
from utils import *

bom_headers = ['bom_id', 'name_prefix', 'devicetype_id',
               'controllertype_id', 'emplacement_id', 'floor_name']
profile_headers = ['name_prefix', 'devicetype_id',
                   'controllertype_id', 'emplacement_id', 'floor_name']


def combo_box_Initialize(ui):
    options = db_handle.select_data('bom', ['bom_name'])
    for option in options:
        ui.bomComboBox.addItem(option[0])
    device_type = db_handle.select_data('device_type', ['device_type_name'])
    for option in device_type:
        ui.deviceTypeComboBox.addItem(option[0])
    emplacement_type = db_handle.select_data(
        'emplacement_type', ['emplacement_name'])
    for option in emplacement_type:
        ui.locationComboBox.addItem(option[0])
    controller_type = db_handle.select_data(
        'controller_type', ['controller_type_name'])
    for option in controller_type:
        ui.controllerTypeComboBox.addItem(option[0])


def search_event(ui, item_type):
    if item_type == 'edge':
        keyword = ui.edgeSearchLineEdit.text()
        data_list = db_handle.search_value('edge_device', 'edge_id', keyword)
        ui.edgeComboBox.clear()
        for option in data_list:
            ui.edgeComboBox.addItem(option[0])
    elif item_type == 'child':
        keyword = ui.childSearchLineEdit.text()
        data_list = db_handle.search_value('child_device', 'child_id', keyword)
        ui.childComboBox.clear()
        for option in data_list:
            ui.childComboBox.addItem(option[0])


def edge_combo_changed_event(ui):
    query = """
            SELECT n.note_detail
            FROM edge_device AS e
            JOIN note AS n ON e.note_id = n.note_id
            WHERE e.edge_id = %s
        """
    value = ui.edgeComboBox.currentText().strip()
    if not value:
        return
    note = db_handle.execute_query(query, (value,))
    if len(note) != 0:
        note = note[0][0]
        ui.noteTextBrowser.setText(note)
    else:
        ui.noteTextBrowser.setText("")


def bom_combobox_changed_event(ui):
    processed_config_list = []
    header = ['name_prefix', 'device_type',
              'controller_type', 'location', 'room']

    value = ui.bomComboBox.currentText()
    query = f"""
            SELECT dp.name_prefix, dt.device_type_name, ct.controller_type_name, et.emplacement_name, dp.floor_name
            FROM device_profile dp
            JOIN controller_type ct ON dp.controller_type_id = ct.controller_type_id
            JOIN device_type dt ON dp.device_type_id = dt.device_type_id
            JOIN emplacement_type et ON dp.emplacement_id = et.emplacement_id
            JOIN bom b ON dp.deprofile_id = b.deprofile_id
            WHERE b.bom_name = '{value}';
        """
    config_list = db_handle.execute_query(query)
    populate_table(ui.groupListTableView, header, config_list)


def refresh_bom_event(ui):
    ui.bomComboBox.clear()
    box_id_list = db_handle.select_data('bom', ['bom_name'])
    for box_id in box_id_list:
        ui.bomComboBox.addItem(box_id[0])


def add_bom_event(ui):
    bom_name = ui.bomNameLineEdit.text()
    if bom_name is None or bom_name in ('', []):
        show_warning_window("Please fill the bom name!")
        return
    data = get_data_from_table_view(ui.bomTableView)

    check_name_duplicate = f'''
    SELECT COUNT(*) as name_count
    FROM bom
    WHERE bom_name = '{bom_name}';
    '''
    is_duplicate = db_handle.execute_query(check_name_duplicate)[0][0]
    if is_duplicate:
        show_warning_window("This name is already existed")
        return

    if data == []:
        show_warning_window("Please add more profile!")
        return
    profile_idx = []
    for row in data:
        name_prefix = row[0]
        devicetype_id = db_handle.select_data('device_type', [
            'device_type_id'], f"device_type_name='{row[1]}'")[0][0]
        controllertype_id = db_handle.select_data('controller_type', [
            'controller_type_id'], f"controller_type_name='{row[2]}'")[0][0]
        emplacement_id = db_handle.select_data('emplacement_type', [
            'emplacement_id'], f"emplacement_name='{row[3]}'")[0][0]
        floor_name = row[4]
        processed_data = [name_prefix, devicetype_id,
                          controllertype_id, emplacement_id, floor_name]
        inserted_data = dict(zip(profile_headers, processed_data))
        db_handle.insert_data('device_profile', inserted_data)

        # Retrieve the last inserted ID
        query_get_last_id = 'SELECT LAST_INSERT_ID() AS deprofile_id'
        last_inserted_id = db_handle.execute_query(query_get_last_id)[0][0]
        profile_idx.append(last_inserted_id)

    get_lowest_bom_id_query = '''
        SELECT COALESCE(MIN(bom_id) + 1, 0)  AS lowest_unused_number
        FROM bom
        WHERE (bom_id + 1) NOT IN (SELECT bom_id FROM bom);
    '''
    lowest_bom_id = db_handle.execute_query(get_lowest_bom_id_query)[0][0]
    bom_header = ['bom_id', 'bom_name', 'deprofile_id']
    for idx in profile_idx:
        db_handle.insert_data('bom', dict(
            zip(bom_header, [lowest_bom_id, bom_name, idx])))
    populate_table(ui.bomTableView, profile_headers, [])


def add_profile_event(ui):
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
        populate_table(ui.bomTableView, profile_headers, data)
    else:
        show_warning_window("All data must be selected!")
        return


def clear_group_event(ui):
    populate_table(ui.bomTableView, profile_headers, [])


def add_group_event(ui):
    bom_name = ui.bomComboBox.currentText()
    bom_id = db_handle.select_data(
        'bom', ['bom_id'], f"bom_name='{bom_name}'")[0][0]
    edge_id = ui.edgeComboBox.currentText()
    child_id = ui.childComboBox.currentText()
    if edge_id == '' or child_id == '' or bom_id == '':
        ui.addStatusLabel.setText('<span style="color: red;">Fail!</span>')
        show_warning_window("Please select all data!")
        return
    kitting_device = {
        'edge_id': edge_id,
        'child_id': child_id,
        'datetime': get_date_time()
    }
    db_handle.insert_data('kitting_device', kitting_device)
    db_handle.update_value('child_device', 'bom_id',
                           bom_id, f"child_id='{child_id}'")
    ui.addStatusLabel.setText('<span style="color: green;">Success!</span>')


if __name__ == '__main__':
    pass
