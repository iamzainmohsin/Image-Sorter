import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QWidget
from ui.ui_main_window import Ui_MainWindow
from ui.ui_images_container import Ui_imagesContainer
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QSize


class Image_Viewer(QWidget, Ui_imagesContainer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.image_paths = []
        self.folder_paths = []
        self.current_image_index = 0
        self.current_folder_index = 0

        self.nextImageButton.clicked.connect(self.nextImageButton)
        












class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.selectedFolderPath = None
        self.selectFolderButton.clicked.connect(self.selectFolder)


    def scanImages(self, folder_path):
        allImages = []
        IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.tiff')

        if not folder_path:
            print("Nothing was selected")
            return allImages
        
        if not os.path.isdir(folder_path):
            print(f"{folder_path} is not a valid directory")
            return allImages
        
        for img_name in os.listdir(folder_path):
            full_path = os.path.join(folder_path, img_name)

            if os.path.isfile(full_path):
                if img_name.lower().endswith(IMAGE_EXTENSIONS):
                    allImages.append(full_path)

        return  allImages     


    def selectFolder(self):
        homeDir = os.path.expanduser('~')
        folder_path = QFileDialog.getExistingDirectory(self, "Select Image Folder", homeDir)

        if folder_path:
            self.selectedFolderPath = folder_path
            print(f"Selected Folder Path: {self.selectedFolderPath}")
            found_images = self.scanImages(self.selectedFolderPath)

            if found_images:
                for images in found_images:
                    print(images)
            else:
                print("No image found")        


        else:
            print("No folder was selected")    


if __name__ == "__main__":
    application = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(application.exec())            