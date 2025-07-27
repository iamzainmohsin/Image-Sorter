import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui.ui_main_window import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.selectFolderButton.clicked.connect(self.selectFolder)

    def selectFolder(self):
        print("You clicked the button")


if __name__ == "__main__":
    application = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(application.exec())            