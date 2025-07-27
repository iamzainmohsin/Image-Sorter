import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui.ui_main_window import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.selectedFolderPath = None
        self.selectFolderButton.clicked.connect(self.selectFolder)

    def selectFolder(self):
        homeDir = os.path.expanduser('~')

        folderPath = QFileDialog.getExistingDirectory(self, "Select Image Folder", homeDir)

        if folderPath:
            self.selectedFolderPath = folderPath
            print(f"Selected Folder Path: {self.selectedFolderPath}")
        else:
            print("No folder was selected")    


if __name__ == "__main__":
    application = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(application.exec())            