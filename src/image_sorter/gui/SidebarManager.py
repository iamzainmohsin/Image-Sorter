from imports import os, QIcon, QPixmap, Qt, QTimer, QListWidget, QListWidgetItem, ThreadPoolExecutor, QFileDialog 

class SidebarManager:
    def __init__(self, main_window, image_manager, list_widget:QListWidget):
        self.list_widget = list_widget
        self.image_manager = image_manager
        self.main_window = main_window
        self.thumbnail_cache = {}
        self.thumbnail_size = 100
        self.executor = ThreadPoolExecutor(max_workers=3)

    #Selects Images:
    def add_images(self):        
        path = self.image_manager.get_current_image_path()

        if path in self.image_manager.selected_images:
            return
                
        if path:
            self.image_manager.selected_images.append(path)
            #Add loading placeholder
            placeholder = QListWidgetItem("Loading image...")
            placeholder.setData(Qt.ItemDataRole.UserRole, path)
            self.list_widget.addItem(placeholder)

            self.executor.submit(self.load_thumbnail, path)   

    #loads thumbnails:
    def load_thumbnail(self, path):
        pixmap = QPixmap(path).scaled(
            self.thumbnail_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        QTimer.singleShot(0, lambda: self.apply_thumbnail(path, pixmap))

    #Apply thumbs
    def apply_thumbnail(self, path, pixmap):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)

            if item.data(Qt.ItemDataRole.UserRole) == path:
                item.setIcon(QIcon(pixmap))
                item.setText(os.path.basename(path))
                break                

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