# imports.py
# PyQt6 Core and GUI Elements
from PyQt6.QtWidgets import QFileDialog, QListWidgetItem, QListWidget, QStatusBar
from PyQt6.QtGui import QPixmap, QIcon, QImage
from PyQt6.QtCore import Qt, QSize, QTimer, QByteArray, QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot, Qt

# Standard Library
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor

import os

#Local Imports
from image_sorter.backend.ImagesLogicManager import ImagesManager
from image_sorter.gui.PYQT_Ui_File.ui_image_viewer import Ui_MainWindow
from image_sorter.cpp import image_utils
from image_sorter.cpp import thumbnail_utils
from image_sorter.gui.ThumbnailWorker import ThumbnailTask