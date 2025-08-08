from imports import os, QIcon, ThumbnailTask, Qt, QImage, QListWidget, QListWidgetItem, QThreadPool, QFileDialog, thumbnail_utils


class SidebarManager:
    def __init__(self, main_window, image_manager, list_widget:QListWidget):
        self.list_widget = list_widget
        self.image_manager = image_manager
        self.main_window = main_window
        self.thumbnail_cache = {}
        self.thumbnail_size = 30

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
        if self.list_widget.count() == 0:
            print("No items to save")
            return
        
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

        if file_path in self.image_manager.selected_images:
            print(f"Image already selected: {file_path}")
            return
        
        self.image_manager.selected_images.append(file_path)
 
        #Placeholder item
        file_name = os.path.basename(file_path)
        part = file_name[:20] + "...."
        placeholder_item = QListWidgetItem(f"Loading Image... {part}")
        placeholder_item.setData(Qt.ItemDataRole.UserRole, file_path)
        self.list_widget.addItem(placeholder_item)
        self.thumbnail_cache[file_path] = placeholder_item

        #Launch worker
        task = ThumbnailTask(file_path, self.thumbnail_size)
        task.signals.finished.connect(self._on_thumnail_ready)
        task.signals.error.connect(self.on_thumbnail_error)
        QThreadPool.globalInstance().start(task)


    def _on_thumnail_ready(self, file_path, pixmap, elapsed_time):
        if file_path in self.thumbnail_cache:
            item = self.thumbnail_cache[file_path]
            item.setIcon(QIcon(pixmap))
            item.setText(os.path.basename(file_path))
            del self.thumbnail_cache[file_path]
        print(f"Thumbnail for {file_path} ready in {elapsed_time:.3f} seconds")
          
          
    def on_thumbnail_error(self, file_path, error_msg):
        if file_path in self.thumbnail_cache:
            item = self.thumbnail_cache[file_path]
            item.setText(f"{os.path.basename(file_path)} (Failed)")
            del self.thumbnail_cache[file_path]
        print(f"Failed to add thumbnail for {file_path}: {error_msg}")       
    