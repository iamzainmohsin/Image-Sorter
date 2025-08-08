import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from image_sorter.gui.GuiHandler import GuiHandler

def main():
    app = QApplication(sys.argv)

    try:
        with open("src/image_sorter/gui/PYQT_Ui_File/style.qss", "r") as style_file:
            style_sheet = style_file.read()
            app.setStyleSheet(style_sheet)
    except FileNotFoundError:
        print("Style sheet file not found.")

    main_window = QMainWindow()
    gui = GuiHandler(main_window)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
