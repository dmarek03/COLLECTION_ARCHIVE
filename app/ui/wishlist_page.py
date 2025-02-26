import sys
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import *
from app.utilities.button_style import main_button_style


class WishListPage(QWidget):
    def __init__(self, stacked_page: QStackedWidget):
        super().__init__()
        self.stacked_page = stacked_page
        self.layout = QGridLayout(self)
        self.init_ui()
        self.item_list = None

    def init_ui(self) -> None:
        name_label = QLabel('Wish List ')
        name_label.setFont(QFont('Cambria Math', 30))

        back_button = QPushButton('Back')
        back_button.setMaximumWidth(200)
        back_button.setStyleSheet(main_button_style)
        back_button.clicked.connect(self.go_to_start_page)

        create_wishlist_button = QPushButton('Create wishlist')
        create_wishlist_button.setMaximumWidth(200)
        create_wishlist_button.setStyleSheet(main_button_style)
        create_wishlist_button.clicked.connect(self.go_to_add_wishlist_page)

        self.layout.addWidget(name_label, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(back_button, 5, 0, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(create_wishlist_button, 5, 1, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

    def show_wishlist(self) -> None:

        frame = QFrame(self)
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setFrameShadow(QFrame.Shadow.Sunken)
        frame.setFixedHeight(200)
        frame.setStyleSheet("background-color: red;")

        self.layout.addWidget(frame, 2, 0, 3, 3, Qt.AlignmentFlag.AlignCenter)
        for item in self.item_list:
            item_layout = QVBoxLayout()
            item_layout.setSpacing(5)
            item_name = QLabel(f'<b>Item name:<b> {item.name}')

            image_label = QLabel()
            item_image = QPixmap()
            item_image.loadFromData(item.image_data)

            image_label.setPixmap(
                item_image.scaled(160, 160, Qt.AspectRatioMode.KeepAspectRatio)
            )

            image_label.setMaximumHeight(160)
            image_label.setMaximumWidth(160)

            item_layout.addWidget(image_label, Qt.AlignmentFlag.AlignCenter)
            item_layout.addWidget(item_name, Qt.AlignmentFlag.AlignCenter)

            self.layout.addLayout(item_layout)

    def go_to_start_page(self) -> None:
        self.stacked_page.setCurrentIndex(0)

    def go_to_add_wishlist_page(self) -> None:
        self.stacked_page.setCurrentIndex(5)

