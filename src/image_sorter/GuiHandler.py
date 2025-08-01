from PyQt6.QtWidgets import QFileDialog, QListWidgetItem
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
from image_sorter.ImagesManager import ImagesManager
from .ui.ui_image_viewer import Ui_MainWindow
import os

class GuiHandler:
    def __init__(self, main_window):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(main_window)
        self.main_window = main_window
        self.image_manager = ImagesManager()
        self.thumbnail_size = QSize(100, 100)
        self.selected_sidebar_path = None
        self.image_display = self.ui.imagePlaceholderLabel 
        self.setup_connections()

    def setup_connections(self):
        self.ui.importFolderButton.clicked.connect(self.import_folder)
        self.ui.nextFolderButton.clicked.connect(self.next_folder)
        self.ui.prevFolderButton.clicked.connect(self.prev_folder)
        self.ui.nextImageButton.clicked.connect(self.next_image)
        self.ui.prevImageButton.clicked.connect(self.prev_image)
        self.ui.selectImageButton.clicked.connect(self.select_current_image)
        self.ui.saveButton.clicked.connect(self.save_selected_images)
        self.ui.removeButton.clicked.connect(self.remove_selected_image)
        self.ui.selectedImagesList.itemClicked.connect(self.image_manager.handle_sidebar_click)

    def import_folder(self):

        root_folder = QFileDialog.getExistingDirectory(self.main_window, "Select Main Folder")

        if not root_folder:
            print("Folder selection canceled")
            return

        success = self.image_manager.import_folder(root_folder)

        if success:
            self.show_current_image()
        else:
            print("No valid images found.")    

        
    def show_current_image(self):
        folder = self.image_manager.get_current_folder_name()
        image_path = self.image_manager.get_current_image_path()

        if not folder or not image_path:
            self.ui.folder_label.setText("Folder: —")
            self.ui.image_label.setText("Image: —")
            self.image_display.clear()
            # self.image_display.setText("Folder seems to be empty")
            return 


        self.ui.folder_label.setText(f"Folder: {os.path.basename(folder)}")
        index = self.image_manager.get_current_image_index()
        total = self.image_manager.get_current_folder_image_count()
        self.ui.image_label.setText(f"Image: ({index + 1} of {total})")

        pixmap = QPixmap(image_path)
        scaled = pixmap.scaled(
            self.image_display.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_display.setPixmap(scaled)


    def next_folder(self):
            self.image_manager.next_fld_btn()
            self.show_current_image()

    def prev_folder(self):
        self.image_manager.prev_fld_btn()
        self.show_current_image()

    def next_image(self):
        self.image_manager.next_img_btn()
        self.show_current_image()
        
        
    def prev_image(self):
        self.image_manager.prev_img_btn()
        self.show_current_image()


    def select_current_image(self):
        current_path = self.image_manager.get_current_image_path()

        if current_path and current_path not in self.image_manager.selected_images:
            self.image_manager.selected_images.append(current_path)
            self.update_selected_thumbnails()  

    

    def remove_selected_image(self):
        self.image_manager.rmv_img_btn()
        self.update_selected_thumbnails() 


    def update_selected_thumbnails(self):
        self.ui.selectedImagesList.clear()
        for path in self.image_manager.selected_images:
            item = QListWidgetItem()
            icon = QIcon(QPixmap(path). scaled(self.thumbnail_size, Qt.AspectRatioMode.KeepAspectRatio))
            item.setIcon(icon)
            item.setText(os.path.basename(path))
            self.ui.selectedImagesList.addItem(item)


    def save_selected_images(self):
        target_folder = QFileDialog.getExistingDirectory(self.main_window, "Select Folder to Save Images")

        if not target_folder:
            return

        self.image_manager.save_images_to_folder(self.image_manager.selected_images, target_folder)
                     