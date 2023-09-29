import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QAbstractItemView, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem


def delete_selected_row(table_view):
    selected_indexes = table_view.selectionModel().selectedRows()

    if not selected_indexes:
        QMessageBox.warning(
            None,
            "Warning",
            "No row selected. Please select a row to delete.",
            QMessageBox.Ok,
        )
        return

    selected_indexes.sort(reverse=True)

    model = table_view.model()
    for index in selected_indexes:
        model.removeRow(index.row())

    table_view.clearSelection()


app = QApplication(sys.argv)
window = QMainWindow()
central_widget = QWidget()
window.setCentralWidget(central_widget)

layout = QVBoxLayout(central_widget)

model = QStandardItemModel()
model.setColumnCount(3)
model.setHorizontalHeaderLabels(["Name", "Age", "Country"])

for name, age, country in [("Alice", 25, "USA"), ("Bob", 30, "Canada"), ("Charlie", 22, "UK")]:
    row = [QStandardItem(name), QStandardItem(
        str(age)), QStandardItem(country)]
    model.appendRow(row)

table_view = QTableView()
table_view.setModel(model)
table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
table_view.setSelectionMode(QAbstractItemView.MultiSelection)

layout.addWidget(table_view)

delete_button = QPushButton("Delete Selected Row(s)")
delete_button.clicked.connect(lambda: delete_selected_row(table_view))
layout.addWidget(delete_button)

window.show()
sys.exit(app.exec_())
