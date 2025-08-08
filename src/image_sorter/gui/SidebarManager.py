from imports import os, QIcon, QPixmap, Qt, QImage,QTimer, QListWidget, QListWidgetItem, ThreadPoolExecutor, QFileDialog, QByteArray, image_utils, thumbnail_utils,np, cv2 

class SidebarManager:
    def __init__(self, main_window, image_manager, list_widget:QListWidget):
        self.list_widget = list_widget
        self.image_manager = image_manager
        self.main_window = main_window
        self.thumbnail_cache = {}
        self.thumbnail_size = 30
        self.executor = ThreadPoolExecutor(max_workers=3)

    #Removes the image:
    def remove_image(self):
        item_to_remove = self.list_widget.currentItem()
        
        if item_to_remove is None:
            print("No item to remove")
            return
        
        path = item_to_remove.data(Qt.ItemDataRole.UserRole)

        if path in self.image_manager.selected_images:
            self.image_manager.selected_images.remove(path)
            
        self.list_widget.takeItem(self.list_widget.row(item_to_remove))


    #Saves the image:
    def save_images(self):
        target_folder = QFileDialog.getExistingDirectory(self.main_window, "Select Folder to Save Images")

        if not target_folder:
            return
        
        self.image_manager.save_images_to_folder(self.image_manager.selected_images, target_folder)
        self.clear()


    #clear the list:
    def clear(self):
        self.image_manager.selected_images.clear()
        self.list_widget.clear()    

    #Selecting Images:
    def add_images(self):
        file_path = self.image_manager.get_current_image_path()

        if not file_path:
            print("No selected images to add")
            return

        if file_path not in self.image_manager.selected_images:
            self.image_manager.selected_images.append(file_path)

        try:

            arr = thumbnail_utils.get_resized_thumbnail(file_path, self.thumbnail_size, self.thumbnail_size)
            qImg = QImage(
                arr.data, arr.shape[1], arr.shape[0], arr.strides[0],
                QImage.Format.Format_BGR888
            )
            pixmap = QPixmap.fromImage(qImg)
            item = QListWidgetItem(QIcon(pixmap), os.path.basename(file_path))
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            self.list_widget.addItem(item)

        except Exception as e:
            print(f"Failed to add thumbnail for {file_path}: {e}")
    