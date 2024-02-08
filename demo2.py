import xml.etree.ElementTree as ET
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Song List")
        self.setStyleSheet("background-color: black;")

        self.song_list_widget = QListWidget(self)
        self.song_list_widget.setStyleSheet("color: white;")

        # Load songs from the provided NML file
        self.load_songs_from_xml("BREAK_ALL.nml")
        self.setCentralWidget(self.song_list_widget)

    def load_songs_from_xml(self, file_path):
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Find all 'ENTRY' elements and extract song information
        for entry in root.findall(".//ENTRY"):
            title = entry.get('TITLE')
            artist = entry.get('ARTIST')
            # Check if both title and artist are found
            if title and artist:
                song_info = f"{title} - {artist}"
                self.song_list_widget.addItem(song_info)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()