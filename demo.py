import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide Example")
        self.setStyleSheet("background-color: black;")

        self.button = QPushButton("Click me", self)
        self.button.setStyleSheet("QPushButton {color: white;}"
                                  "QPushButton:hover {background-color: grey;}")
        self.button.clicked.connect(self.on_button_clicked)

        self.setCentralWidget(self.button)

    def on_button_clicked(self):
        self.button.setStyleSheet("QPushButton {color: white; background-color: red;}"
                                  "QPushButton:hover {background-color: grey;}")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())