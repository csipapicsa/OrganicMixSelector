import sys
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag

class DraggableTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def startDrag(self, supportedActions):
        indexes = self.selectedIndexes()
        if indexes:
            mimeData = self.mimeData(indexes)
            if mimeData.hasUrls():
                drag = QDrag(self)
                drag.setMimeData(mimeData)
                drag.exec_(Qt.CopyAction | Qt.MoveAction)

    def mimeData(self, indexes):
        mimeData = QMimeData()
        urlList = []
        for index in indexes:
            if index.column() == 0:  # Assuming the file path is in the first column
                filePath = self.item(index.row(), index.column()).data(Qt.UserRole)
                urlList.append(QUrl.fromLocalFile(filePath))
        mimeData.setUrls(urlList)
        return mimeData

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Song List")
        self.setStyleSheet("background-color: black;")

        self.table_widget = DraggableTableWidget(0, 2, self)
        self.table_widget.setHorizontalHeaderLabels(['Artist', 'Title'])
        self.table_widget.setStyleSheet("QHeaderView::section { color: white; }")
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setSortingEnabled(True)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)

        self.load_songs_from_xml("BREAK_ALL.nml")

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_songs_from_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        for entry in root.findall(".//ENTRY"):
            artist = entry.get('ARTIST')
            title = entry.get('TITLE')
            try:
                file_path = entry.find('.//LOCATION').get('FILE')
                dir_path = entry.find('.//LOCATION').get('DIR').replace(':/','').replace(':','/')
                full_path = dir_path + file_path  # Construct the full file path
            except:
                full_path = None
                print("No file path found for", artist, title)
            
            

            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(artist))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(title))
            # Store the full file path in the item's UserRole data
            self.table_widget.item(row_position, 0).setData(Qt.UserRole, full_path)

        self.table_widget.resizeColumnsToContents()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()