import sys
import os 
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMainWindow
from PyQt6.QtCore import Qt, QUrl, QMimeData

class FolderDropArea(QWidget):
    def __init__(self, parent = None, on_folders_dropped = None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.on_folders_dropped = on_folders_dropped

    def dragEnterEvent(self, event):
        if self.contains_valid_folder(event):
            event.acceptProposedAction()
        else:
            event.ignore()  

    def dropEvent(self, event):
        folder_paths = self.extract_folder_paths(event)

        if folder_paths:
            if self.on_folders_dropped:
                self.on_folders_dropped(folder_paths)
            print(f"Dropped {len(folder_paths)} folder(s)")
            
        else:
            print("No valid folders dropped")     

        event.acceptProposedAction()            


    def contains_valid_folder(self, event):
        for url in event.mimeData().urls():
            if url.isLocalFile() and os.path.isdir(url.toLocalFile()):
                return True
        return False

    def extract_folder_paths(self, event):
        return [
            url.toLocalFile()
            for url in event.mimeData().urls()
            if url.isLocalFile() and os.path.isdir(url.toLocalFile())
        ]




























 