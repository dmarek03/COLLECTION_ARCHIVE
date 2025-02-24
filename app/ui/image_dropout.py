from PyQt6.QtCore import Qt, QDir, QSize, QByteArray, QBuffer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QWidget, QPushButton, QGridLayout, QFileDialog


class PhotoLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self) -> None:
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("\n\n Drop Image Here \n\n")
        self.setStyleSheet(
            """
        QLabel {
            border: 4px dashed #aaa;
        }"""
        )

    def setPixmap(self, *args, **kwargs):
        super().setPixmap(*args, **kwargs)
        self.setStyleSheet(
            """
        QLabel {
            border: none;
        }"""
        )

    def is_empty(self):

        return self.pixmap() is None or self.pixmap().isNull()


class PhotoDropout(QWidget):

    def __init__(self):
        super().__init__()
        self.photo = PhotoLabel()
        btn = QPushButton("Browse")
        btn.clicked.connect(self.open_image)
        grid = QGridLayout(self)
        grid.addWidget(btn, 0, 0, Qt.AlignmentFlag.AlignHCenter)
        grid.addWidget(self.photo, 1, 0)
        self.setAcceptDrops(True)
        self.resize(300, 200)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.DropAction.CopyAction)
            filename = event.mimeData().urls()[0].toLocalFile()
            event.accept()
            self.open_image(filename)
        else:
            event.ignore()

    # TODO Think about showing scaled image but saving data from original image
    def open_image(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Select Photo", QDir.currentPath(), "Images (*.png *.jpg *.jpeg)"
            )
            if not filename:
                return

        pixmap = QPixmap(filename)
        min_size = QSize(200, 200)
        max_size = QSize(400, 400)

        scaled_pixmap = pixmap.scaled(
            max_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        if (
            scaled_pixmap.width() < min_size.width()
            or scaled_pixmap.height() < min_size.height()
        ):
            scaled_pixmap = pixmap.scaled(
                min_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        self.photo.setPixmap(scaled_pixmap)

    def get_image(self):
        if not self.photo.is_empty():
            return self.photo.pixmap()
        return None

    def clear(self) -> None:
        self.photo.clear()
        self.photo.init_ui()

    def convert_to_bytes(self):
        if pixmap := self.get_image():
            image = pixmap.toImage()
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QBuffer.OpenModeFlag.WriteOnly)
            image.save(buffer, format="JPEG")
            return byte_array.data()
