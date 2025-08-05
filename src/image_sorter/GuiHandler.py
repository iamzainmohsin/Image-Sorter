from PyQt6.QtWidgets import QFileDialog, QListWidgetItem
from PyQt6.QtGui import QPixmap, QIcon, QImage
from PyQt6.QtCore import Qt, QSize, QTimer
from image_sorter.ImagesManager import ImagesManager
from .ui.ui_image_viewer import Ui_MainWindow
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from .cpp import image_utils
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
        self.processor = image_utils.ImageProcessor()
        self.image_cache = {}
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.thumbnail_cache = {}
        self.thumbnail_executor = ThreadPoolExecutor(max_workers=2)
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

        
        # #Image Processed through C++
        target_size = self.image_display.size()
        label_width = target_size.width()
        label_height = target_size.height()

        if image_path in self.image_cache:
            current_pixmap = self.image_cache[image_path]
        else:
            if self.processor.load_image(image_path) and self.processor.resize_image(label_width, label_height):
                np_img = self.processor.get_image_copy()
                current_pixmap = self.cv_to_qpixmap(np_img)
                self.image_cache[image_path] = current_pixmap
            else:
                self.image_display.setText("Failed to process image")
                return

        self.image_display.setPixmap(current_pixmap)

        # Preload next
        next_path = self.image_manager.peek_next_img()
        if next_path and next_path not in self.image_cache:
            self.executor.submit(self.preload_images, next_path)
    
        
    


    def next_folder(self):
            self.image_manager.next_fld_btn()
            self.show_current_image()

    def prev_folder(self):
        self.image_manager.prev_fld_btn()
        self.show_current_image()

    def next_image(self):
        next_path = self.image_manager.peek_next_img()

        if next_path and next_path not in self.image_cache:
            self.ui.nextImageButton.setEnabled(False)

            QTimer.singleShot(50, lambda: (
                self.ui.nextImageButton.setEnabled(True),
                self.image_manager.next_img_btn(),
                self.show_current_image()
            ))
        else:
            self.image_manager.next_img_btn()
            self.show_current_image()
    
        
        
    def prev_image(self):
        self.image_manager.prev_img_btn()
        self.show_current_image()


    def select_current_image(self):
        current_path = self.image_manager.get_current_image_path()

        if current_path and current_path not in self.image_manager.selected_images:
            self.image_manager.selected_images.append(current_path)

            item = QListWidgetItem("Loading...")
            item.setData(Qt.ItemDataRole.UserRole, current_path)
            self.ui.selectedImagesList.addItem(item)

            if current_path in self.thumbnail_cache:
                # Apply immediately from cache
                self.apply_thumbnail(current_path, self.thumbnail_cache[current_path])
            else:
                # Load in background
                self.thumbnail_executor.submit(self.load_thumbnail, current_path)  

    

    def remove_selected_image(self):
        self.image_manager.rmv_img_btn()
        self.update_selected_thumbnails() 


    def update_selected_thumbnails(self):
        self.ui.selectedImagesList.clear()

        for path in self.image_manager.selected_images:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, path)

            if path in self.thumbnail_cache:
                item.setIcon(QIcon(self.thumbnail_cache[path]))
                item.setText(os.path.basename(path))
            else:
                item.setText("Loading...")
                self.thumbnail_executor.submit(self.load_thumbnail, path)

            self.ui.selectedImagesList.addItem(item)


    def load_thumbnail(self, path):
        pixmap = QPixmap(path).scaled(
            self.thumbnail_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        if not pixmap.isNull():
            self.thumbnail_cache[path] = pixmap

        QTimer.singleShot(0, lambda: self.apply_thumbnail(path, pixmap))



    def apply_thumbnail(self, path, pixmap):
        for i in range(self.ui.selectedImagesList.count()):
            item = self.ui.selectedImagesList.item(i)
            stored_path = item.data(Qt.ItemDataRole.UserRole)

            if stored_path == path:
                item.setIcon(QIcon(pixmap))
                item.setText(os.path.basename(path))
                break


    
    def save_selected_images(self):
        target_folder = QFileDialog.getExistingDirectory(self.main_window, "Select Folder to Save Images")

        if not target_folder:
            return

        self.image_manager.save_images_to_folder(self.image_manager.selected_images, target_folder)
        
                     

    #C++ to python setup functions:
    def cv_to_qpixmap(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        height, width, channels = rgb_image.shape
        bytes_per_line = rgb_image.strides[0]
    
        qimg = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(qimg)                 
    

    #Multi Threading:
    def preload_images(self, image_path):
        if not image_path or image_path in self.image_cache:
            return

        target_size = self.image_display.size()
        label_width = target_size.width()
        label_height = target_size.height()
 
        if self.processor.load_image(image_path) and self.processor.resize_image(label_width, label_height):
            np_img = self.processor.get_image_copy()
            pixmap = self.cv_to_qpixmap(np_img)
            self.image_cache[image_path] = pixmap
        
