import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.ui_image_viewer import Ui_MainWindow

class Main_UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.stacked_main.setCurrentIndex(0)
        self.ui.importFld_btn.clicked.connect(self.handle_import)


    def handle_import(self):
        print("Import Folder button clicked")    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_UI()
    window.show()
    sys.exit(app.exec())