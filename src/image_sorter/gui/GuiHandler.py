from imports import *
from image_sorter.gui.SidebarManager import SidebarManager
from image_sorter.gui.ImageDisplayManager import ImageDisplay


class GuiHandler:
    def __init__(self, main_window):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(main_window)
        self.main_window = main_window
        self.image_manager = ImagesManager()
        self.sidebar = SidebarManager(self.ui.statusbar, self.main_window, self.image_manager, self.ui.selectedImagesList)
        self.navigation = ImageDisplay(self.ui.statusbar, self.main_window, self.image_manager, self.ui)
        self.setup_connections()

    def setup_connections(self):
        self.ui.importFolderButton.clicked.connect(self.navigation.import_folder)
        self.ui.selectImageButton.clicked.connect(self.sidebar.add_images)
        self.ui.nextImageButton.clicked.connect(self.navigation.next_image)
        self.ui.prevImageButton.clicked.connect(self.navigation.prev_image)
        self.ui.nextFolderButton.clicked.connect(self.navigation.next_folder)
        self.ui.prevFolderButton.clicked.connect(self.navigation.prev_folder)
        self.ui.saveButton.clicked.connect(self.sidebar.save_images)
        self.ui.removeButton.clicked.connect(self.sidebar.remove_image)
  