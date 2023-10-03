from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime


def populate_table(table_view, headers, data):
    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(headers)

    for row_data in data:
        row_items = [QStandardItem(str(cell)) for cell in row_data]
        model.appendRow(row_items)

    table_view.setModel(model)


def get_data_from_table_view(table_view):
    model = table_view.model()
    if not model:
        return []

    data = []
    for row in range(model.rowCount()):
        row_data = []
        for column in range(model.columnCount()):
            item = model.item(row, column)
            if item is not None:
                row_data.append(item.text())
            else:
                row_data.append("")  # Handle empty cells

        data.append(row_data)

    return data


def delete_selected_row(table_view):
    # Get the currently selected row(s)
    try:
        selected_indexes = table_view.selectionModel().selectedRows()

        if not selected_indexes:
            QMessageBox.warning(
                None,
                "Warning",
                "No row selected. Please select a row to delete.",
                QMessageBox.Ok,
            )
            return

        # Sort the selected indexes in reverse order to avoid index shifting
        selected_indexes.sort(reverse=True)

        # Remove the selected rows from the model
        model = table_view.model()
        for index in selected_indexes:
            model.removeRow(index.row())

        # Clear the selection
        table_view.clearSelection()
    except:
        QMessageBox.warning(
            None,
            "Warning",
            "No row selected. Please select a row to delete.",
            QMessageBox.Ok,
        )
        return


def get_date_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d,%H:%M:%S")


def send_request():
    pass
