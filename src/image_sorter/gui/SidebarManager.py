from imports import os, QIcon, QPixmap, Qt, QTimer, QListWidget, QListWidgetItem, ThreadPoolExecutor 

class SidebarManager:
    def __init__(self, list_widget:QListWidget):
        self.list_widget = list_widget
        self.selected_images = []
        self.thumbnail_cache = {}
        self.thumbnail_size = 100
        self.executor = ThreadPoolExecutor(max_workers=3)

    #Adds Images:
    def add_images(self, path):
        if path in self.selected_images:
            return
        
        self.selected_images.append(path)
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
    def remove_image(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        if path in self.selected_images:
            self.selected_images.remove(path)
        self.list_widget.takeItem(self.list_widget.row(item))

    #clear the list:
    def clear(self):
        self.selected_images.clear()
        self.list_widget.clear()    