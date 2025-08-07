from imports import os, QIcon, QPixmap, Qt, QImage,QTimer, QListWidget, QListWidgetItem, ThreadPoolExecutor, QFileDialog, QByteArray, image_utils, np, cv2 

class SidebarManager:
    def __init__(self, main_window, image_manager, list_widget:QListWidget):
        self.list_widget = list_widget
        self.image_manager = image_manager
        self.main_window = main_window
        self.thumbnail_cache = {}
        self.thumbnail_size = 100
        self.placeholder_pixmap = QPixmap("assets/loading.png")
        self.executor = ThreadPoolExecutor(max_workers=3)

    #Selects Images:
    def add_images(self):        
        path = self.image_manager.get_current_image_path()
        if not path:
            print("[DEBUG] No current image path.")
            return

        for i in range(self.list_widget.count()):
            if self.list_widget.item(i).data(Qt.ItemDataRole.UserRole) == path:
                print("[DEBUG] Image already selected.")
                return

        print(f"[DEBUG] Adding image to sidebar: {path}")
        self.image_manager.selected_images.append(path)

        item = QListWidgetItem("Loading image...")
        item.setData(Qt.ItemDataRole.UserRole, path)
        self.list_widget.addItem(item)

        self._load_thumbnail_data_async(path)  


    # #loads thumbnails:
    def load_thumbnail(self, image_path: str) -> QPixmap:
        try:
            thumb_array = image_utils.ImageProcessor.get_thumbnail_mat(image_path, 128, 128)
            if thumb_array is None:
                print(f"[DEBUG] Thumbnail data is None for {image_path}")
                return self.placeholder_pixmap
            thumb_array = np.ascontiguousarray(thumb_array)

            height, width, channels = thumb_array.shape
            if channels != 3:
                print(f"[DEBUG] Unexpected channel count: {channels}")
                return self.placeholder_pixmap

            # Step 4: Convert to QImage and then QPixmap
            image = QImage(thumb_array.data, width, height, width * channels, QImage.Format_RGB888)
            return QPixmap.fromImage(image)

        except Exception as e:
            print(f"[ERROR] Thumbnail fetch failed for {image_path}: {e}")
            return self.placeholder_pixmap



    # #Apply thumbs
    def apply_thumbnail(self, path, pixmap):
        print(f"[DEBUG] Applying thumbnail for: {path}")

        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == path:
                item.setIcon(QIcon(pixmap))
                item.setText(os.path.basename(path))
                print(f"[DEBUG] Thumbnail applied for: {path}")
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


    # #thumbnail Multithreading:
    def _load_thumbnail_data_async(self, image_path: str):
        future = self.executor.submit(self._get_thumbnail_data, image_path)
        future.add_done_callback(
            lambda f: QTimer.singleShot(0, lambda: self._on_thumbnail_data_ready(image_path, f.result()))
        )
    

    def _get_thumbnail_data(self, image_path: str) -> bytes:
        try:
            # This is a C++ call and is thread-safe. It returns bytes.
            data = image_utils.get_thumbnail_mat(image_path, 120, 120)
            return data
        except Exception as e:
            print(f"Failed to load thumbnail data for {image_path}: {e}")
            return b'' # Return an empty bytes object on error
        

    def _on_thumbnail_data_ready(self, path: str, data: bytes):
        if not data:
            print(f"[DEBUG] No thumbnail data received for {path}")
            return

        pixmap = QPixmap()
        if not pixmap.loadFromData(QByteArray(data), "WEBP"):
            print(f"[DEBUG] Failed to create QPixmap from data for {path}")
            return
        
        print(f"[DEBUG] QPixmap created successfully for {path}")
        self.apply_thumbnail(path, pixmap)    
   