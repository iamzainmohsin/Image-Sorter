import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout
from ui.ui_image_viewer import Ui_MainWindow

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
       
  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec())

