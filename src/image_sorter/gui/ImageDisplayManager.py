from imports import os, QTimer, QPixmap, cv2, QImage, ThreadPoolExecutor, image_utils, QFileDialog

class ImageDisplay:
    def __init__(self, main_window, image_manager, ui):
        self.image_manager = image_manager
        self.ui = ui
        self.main_window = main_window
        self.image_display = self.ui.imagePlaceholderLabel
        self.processor = image_utils.ImageProcessor()
        self.image_cache = {}
        self.executor = ThreadPoolExecutor(max_workers=3)


    def next_image(self):
        next_path = self.image_manager.peek_next_img()

        if next_path and next_path not in self.image_cache:
            self.ui.nextImageButton.setEnabled(False)

            QTimer.singleShot(50, lambda: (
                self.ui.nextImageButton.setEnabled(True),
                self.image_manager.next_image(),
                self.show_current_image()
            ))
        else:
            self.image_manager.next_image()
            self.show_current_image()


    def prev_image(self):
        self.image_manager.prev_image()
        self.show_current_image()


    def next_folder(self):
        self.image_manager.next_folder()
        self.show_current_image()


    def prev_folder(self):
        self.image_manager.prev_folder()
        self.show_current_image()


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
    