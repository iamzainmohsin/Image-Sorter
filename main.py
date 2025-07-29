import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from ui.ui_image_viewer import Ui_MainWindow

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        
        self.folder_paths = []
        self.current_folder_index = 0
        self.current_img_index = 0


        # Connecting Buttons:
        self.ui.importFolderButton.clicked.connect(self.import_folder)
        self.ui.nextFolderButton.clicked.connect(self.next_fld_btn)
        self.ui.prevFolderButton.clicked.connect(self.prev_fld_btn)
        self.ui.nextImageButton.clicked.connect(self.next_img_btn)
        self.ui.prevImageButton.clicked.connect(self.prev_img_btn)
        self.ui.selectImageButton.clicked.connect(self.select_img_btn)
        self.ui.saveButton.clicked.connect(self.save_img_btn)
        self.ui.removeButton.clicked.connect(self.rmv_img_btn)
        self.image_display = self.ui.imagePlaceholderLabel


    def import_folder(self):

        root_folder = QFileDialog.getExistingDirectory(self, "Choose your Main Folder")

        if not root_folder:
            print("Folder selection canceled")
            return

        sub_folders = []

        for name in os.listdir(root_folder):
            full_path = os.path.join(root_folder, name)
            if os.path.isdir(full_path):
                sub_folders.append(full_path)


        if not sub_folders:
            print("Selected folder has no subfolders or images.")
            return    

        self.folder_paths = sub_folders
        self.collect_images_subfolders()
        
        self.current_folder_index = 0
        self.current_img_index = 0

        self.show_current_image()
        self.next_img_btn()
        self.prev_img_btn()          
        

    

    def collect_images_subfolders(self):
        supported_ext = (".png", ".jpg", ".jpeg", ".raw")
        self.folder_images = {}
        
        for folder in self.folder_paths:
            images = []
            for file in os.listdir(folder):
                if file.lower().endswith(supported_ext):
                    full_path = os.path.join(folder, file)
                    images.append(full_path)

            if images:
                self.folder_images[folder] = images

        print("Collected image paths:")
        for folder, imgs in self.folder_images.items():
            print(f"{folder}: {len(imgs)} image(s)")                


    def show_current_image(self):
        if not self.folder_paths:
            print("No folders available")
            return

        current_folder = self.folder_paths[self.current_folder_index]
        img_list = self.folder_images.get(current_folder, [])

        if not img_list:
            self.image_display.clear()
            print("No images in this folder.")
            return 

        self.current_img_index = max(0, min(self.current_img_index, len(img_list) - 1))

        current_img_path = img_list[self.current_img_index]
        pixmap = QPixmap(current_img_path)
        target_size = pixmap.scaled(self.image_display.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_display.setPixmap(target_size)


        print(f"Showing: {current_img_path}")



    def next_fld_btn(self):
        if self.current_folder_index < len(self.folder_paths) - 1:
            self.current_folder_index += 1
            self.current_img_index = 0
            self.show_current_image()

    def prev_fld_btn(self):
        if self.current_folder_index > 0:
            self.current_folder_index -= 1
            self.current_img_index = 0
            self.show_current_image()

    def next_img_btn(self):
        current_folder = self.folder_paths[self.current_folder_index]
        images = self.folder_images.get(current_folder, [])
        
        if self.current_img_index < len(images) - 1:
            self.current_img_index += 1
            self.show_current_image()
        
        
        

    def prev_img_btn(self):
        if self.current_img_index > 0:
            self.current_img_index -= 1
            self.show_current_image()                         

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

