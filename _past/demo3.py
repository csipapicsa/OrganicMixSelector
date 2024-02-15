import xml.etree.ElementTree as ET
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Song List")
        self.setStyleSheet("background-color: black;")

        # Set up table widget with two columns
        self.table_widget = QTableWidget(0, 2, self)
        self.table_widget.setHorizontalHeaderLabels(['Artist', 'Title'])
        self.table_widget.setStyleSheet("QHeaderView::section { color: white; }")
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setSortingEnabled(True)

        self.load_songs_from_xml("BREAK_ALL.nml")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_songs_from_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        for entry in root.findall(".//ENTRY"):
            title = entry.get('TITLE')
            artist = entry.get('ARTIST')
            if title and artist:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(artist))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(title))

        # Resize columns to content
        self.table_widget.resizeColumnsToContents()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()