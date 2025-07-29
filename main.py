import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from ui.ui_image_viewer import Ui_MainWindow
from ImageGalleryLogic import ImageGalleyLogic

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.imageGalleryLogic = ImageGalleyLogic(self, self.ui)

        # Connecting Buttons:
        self.ui.selectImageButton.clicked.connect(self.select_img_btn)
        self.ui.saveButton.clicked.connect(self.save_img_btn)
        self.ui.removeButton.clicked.connect(self.rmv_img_btn)
                        

    def select_img_btn(self):
        print("Select Image Button Clicked")

    def save_img_btn(self):
        print("Save Image Button Clicked")

    def rmv_img_btn(self):
        print("Remove Image Button Clicked")     











       
  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec())

