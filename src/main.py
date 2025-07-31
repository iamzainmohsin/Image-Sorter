import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from src.image_sorter.GuiHandler import GuiHandler

def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    gui = GuiHandler(main_window)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
