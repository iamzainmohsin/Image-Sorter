import os
import shutil

class ImagesManager:
    SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".raw")

    def __init__(self):
        self.folder_paths = []
        self.selected_images = []
        self.folder_images = {}
        self.current_folder_index = 0
        self.current_img_index = 0
        self.selected_sidebar_path = None


    def import_folder(self, root_folder):
        if not os.path.isdir(root_folder):
            print("Invalid Folder")
            return False

        sub_folders = [ os.path.join(root_folder, name)
                        for name in os.listdir(root_folder)
                        if os.path.isdir(os.path.join(root_folder, name))]

        if not sub_folders:
            print("Empty folder selection")
            return

        self.folder_paths = sub_folders
        self.collect_images()

        self.current_folder_index = 0
        self.current_img_index = 0
        return True


    def collect_images(self):
        self.folder_images.clear()

        for folder in self.folder_paths:
            images = [  os.path.join(folder, file)
                        for file in os.listdir(folder)
                        if file.lower().endswith(self.SUPPORTED_EXTENSIONS)]
            if images:
                self.folder_images[folder] = images


    def get_current_image_path(self):
        if not self.folder_paths:
            return None

        current_folder = self.folder_paths[self.current_folder_index]
        img_list = self.folder_images.get(current_folder, [])

        if not img_list:
            return None

        self.current_img_index = max(0, min(self.current_img_index, len(img_list) - 1))

        return img_list[self.current_img_index]


    def next_folder(self):
        if self.current_folder_index < len(self.folder_paths) - 1:
            self.current_folder_index += 1
            self.current_img_index = 0   


    def prev_folder(self):
        if self.current_folder_index > 0:
            self.current_folder_index -= 1
            self.current_img_index = 0


    def next_image(self):
        current_folder = self.folder_paths[self.current_folder_index]
        images = self.folder_images.get(current_folder, [])
        
        if not self.folder_paths:
            print("No folders loaded.")
            return
        
        if self.current_img_index < len(images) - 1:
            self.current_img_index += 1


    def prev_image(self):
        if self.current_img_index > 0:
            self.current_img_index -= 1


    def remove_image(self):
        if self.selected_sidebar_path in self.selected_images:
            self.selected_images.remove(self.selected_sidebar_path)
            print(f"Removed Selection: {self.selected_sidebar_path}")
            self.selected_sidebar_path = None
        else:
            print("No Image in selection")


    def save_images_to_folder(self, images, target_folder):
        for path in images:
            try:
                shutil.copy(path, os.path.join(target_folder, os.path.basename(path)))
            except Exception as e:
                print(f"Error copying {path}: {e}")
 
 
    #Preload Images in the background
    def peek_next_img(self):
        if not self.folder_paths:
            return None

        folder_path = self.folder_paths[self.current_folder_index]
        images = self.folder_images.get(folder_path, [])
        
        index = self.current_img_index + 1
        if index < len(images):
            return images[index]
        return None


    # The following methods should be triggered by GUI:       
    def clear_selection(self):
        return self.selected_images.clear()            
    
    def get_selected_images(self):
        return self.selected_images.copy()
    
    def get_current_folder_name(self):
        if self.folder_paths:
            return os.path.basename(self.folder_paths[self.current_folder_index])
        return ""
    
    def get_current_folder_image_count(self):
        folder = self.folder_paths[self.current_folder_index]
        return len(self.folder_images.get(folder, []))
    
    def get_current_image_index(self):
        return self.current_img_index
    