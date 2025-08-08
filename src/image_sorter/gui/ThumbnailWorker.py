from imports import os, QObject, QRunnable, thumbnail_utils, pyqtSignal, pyqtSlot, Qt, QImage, QIcon, QPixmap, QListWidgetItem
import time, random

class WorkerSignals(QObject):
    finished = pyqtSignal(str, QPixmap, float)
    error = pyqtSignal(str, str)


class ThumbnailTask(QRunnable):
    def __init__(self, file_path, thumbnail_size):
        super().__init__()
        self.file_path = file_path
        self.thumbnail_size = thumbnail_size
        self.signals = WorkerSignals()
    @pyqtSlot()
    def run(self):
        time.sleep(random.uniform(0.5, 1.2))
        start_time = time.perf_counter()
        try:
            arr = thumbnail_utils.get_resized_thumbnail(self.file_path, self.thumbnail_size, self.thumbnail_size)
            qImg = QImage(
                arr.data, arr.shape[1], arr.shape[0], arr.strides[0],
                QImage.Format.Format_BGR888
            )
            pixmap = QPixmap.fromImage(qImg)
            elapsed = time.perf_counter() - start_time
            self.signals.finished.emit(self.file_path, pixmap, elapsed)
        except Exception as e:
            print(f"Failed to add thumbnail for {self.file_path}: {e}")
