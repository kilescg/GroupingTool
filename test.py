import sys
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
import threading


class BarcodeScanner(QObject):
    barcodeScanned = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            barcode_data = input("Scan a barcode (Q to quit): ")
            if barcode_data.upper() == 'Q':
                break
            self.barcodeScanned.emit(barcode_data)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Barcode Scanner Input')

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 380, 280)

        self.barcode_scanner = BarcodeScanner()
        self.barcode_scanner.barcodeScanned.connect(self.on_barcode_scanned)
        self.barcode_scanner_thread = threading.Thread(
            target=self.barcode_scanner.run)
        self.barcode_scanner_thread.start()

    def on_barcode_scanned(self, barcode_data):
        self.text_edit.append(f'Barcode Scanned: {barcode_data}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
