
import math
from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QGridLayout, QSpinBox, QStackedWidget, QMessageBox
)
from app.ui.image_dropout import PhotoDropout
from app.utilities.button_style import main_button_style
from app.ui.wishlist_page import WishListPage
from app.service.dto import CreatFinalWishItemDto
from app.service.final_wish_item_service import FinalWishItemService


class AddWishlistItemsPage(QWidget):
    def __init__(self, wish_item_service: FinalWishItemService, stacked_widget: QStackedWidget):
        super().__init__()
        self.wish_item_service = wish_item_service
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.items_container = QWidget()
        self.items_layout = QVBoxLayout()
        self.items_container.setLayout(self.items_layout)
        self.item_count_selector = QSpinBox()
        self.add_items_button = QPushButton('Add Items')
        self.create_wish_list_button = QPushButton('Create Wish List')
        self.item_list = []
        self.init_ui()

    def init_ui(self) -> None:

        page_label = QLabel('Create Wish List')
        page_label.setFont(QFont("Cambria Math", 30))
        page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        page_label.setMaximumHeight(100)

        selection_layout = QHBoxLayout()
        selection_layout.setSpacing(30)
        selection_layout.setContentsMargins(0, 0, 0, 0)
        item_count_label = QLabel('Select number of items:')
        item_count_label.setFont(QFont("Cambria Math", 15))
        item_count_label.setMaximumWidth(300)
        item_count_label.setMaximumHeight(40)
        item_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.item_count_selector.setRange(5, 20)
        self.item_count_selector.setValue(10)
        self.item_count_selector.setMinimumWidth(100)
        self.item_count_selector.lineEdit().setReadOnly(True)
        self.item_count_selector.setFixedHeight(40)
        self.item_count_selector.setFont(QFont("Cambria Math", 15))
        self.item_count_selector.setAlignment(Qt.AlignmentFlag.AlignCenter)

        selection_layout.addWidget(item_count_label)
        selection_layout.addWidget(self.item_count_selector)
        selection_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.add_items_button.setStyleSheet(main_button_style)
        self.add_items_button.setMaximumWidth(200)
        self.add_items_button.clicked.connect(self.add_items)

        self.create_wish_list_button.setStyleSheet(main_button_style)
        self.create_wish_list_button.setMaximumWidth(200)
        self.create_wish_list_button.setVisible(False)
        self.create_wish_list_button.clicked.connect(self.creat_wish_list)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_items_button, Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.create_wish_list_button, Qt.AlignmentFlag.AlignCenter)

        back_button_layout = QHBoxLayout()
        back_button = QPushButton('Back')
        back_button.setMaximumWidth(200)
        back_button.setStyleSheet(main_button_style)
        back_button.clicked.connect(self.go_back)
        back_button_layout.addWidget(back_button)

        self.layout.addWidget(page_label, Qt.AlignmentFlag.AlignHCenter)
        self.layout.addLayout(selection_layout, Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.items_container, Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(button_layout)
        self.layout.addLayout(back_button_layout, Qt.AlignmentFlag.AlignHCenter)
        self.layout.addStretch(1)

    def add_items(self) -> None:
        self.items_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.items_layout.setSpacing(10)

        season_label = QLabel('Season name')
        season_label.setFont(QFont('Cambria math', 15))
        season_label.setMaximumWidth(150)
        season_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        season = QLineEdit()
        season.setMaximumWidth(250)
        season.setMaximumHeight(30)
        season.setFont(QFont('Cambria math', 15))
        season.setAlignment(Qt.AlignmentFlag.AlignCenter)
        season_layout = QHBoxLayout()
        season_layout.setSpacing(5)
        season_layout.setContentsMargins(0, 0, 0, 0)
        season_layout.addWidget(season_label)
        season_layout.addWidget(season)
        season_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.items_layout.addLayout(season_layout)

        items_count = self.item_count_selector.value()
        row_num = math.ceil(items_count / 5)

        for i in range(row_num):
            row_layout = QHBoxLayout()
            for _ in range(min(8, items_count)):
                widget = QWidget()


                item_layout = QGridLayout()
                item_layout.setSpacing(10)

                image = PhotoDropout()
                image.set_size(w_size=100, h_size=100)
                item_name = QLineEdit()
                item_name.setPlaceholderText('Enter item name')

                item_layout.addWidget(image, 0, 1, Qt.AlignmentFlag.AlignCenter)
                item_layout.addWidget(item_name, 1, 1, Qt.AlignmentFlag.AlignCenter)
                self.item_list.append(
                    (item_name, image, season)
                )

                widget.setLayout(item_layout)
                row_layout.addWidget(widget)

                items_count -= 1
                if items_count <= 0:
                    break

            self.items_layout.addLayout(row_layout)

        self.add_items_button.setVisible(False)
        self.create_wish_list_button.setVisible(True)

    def go_back(self) -> None:
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if isinstance(widget, WishListPage):
                self.stacked_widget.setCurrentWidget(widget)

    def create_wish_items(self) -> None:
        for name, image, season_name in self.item_list:
            final_wish_item = CreatFinalWishItemDto(
                name=name.text(),
                image_data=image.convert_to_bytes(),
                season_name=season_name.text()
            )
            self.wish_item_service.add_wishlist_item(item=final_wish_item)
        self.item_list.clear()

    def creat_wish_list(self) -> None:
        if self.validate_added_items():
            self.create_wish_items()
            QMessageBox.information(self, 'Submission correct', 'Wishlist created successfully')
            wishlist_page = self.stacked_widget.widget(4)
            wishlist_page.init_wishlist_left_bar()
            self.clear_items()
            self.create_wish_list_button.setVisible(False)
            self.add_items_button.setVisible(True)

    @staticmethod
    def reset_style(widget):

        widget.setStyleSheet("")
        widget.setPlaceholderText("")

    def validate_added_items(self) -> bool:

        def mark_invalid(widget: QLineEdit, message: str) -> None:
            widget.setPlaceholderText(message)
            widget.setStyleSheet("color: #ff0000; border: 1px solid red;")
            widget.textChanged.connect(partial(self.reset_style, widget))
            errors.append(message)

        errors = []

        for idx, item_widget in enumerate(self.item_list):
            name_widget, image_widget, season_widget = item_widget
            if not season_widget.text():
                mark_invalid(season_widget, 'Season name is required!')

            if not name_widget.text():
                mark_invalid(name_widget, 'Name is required!')

            if not image_widget.get_image():
                errors.append(f"Item {idx + 1}: Image is missing.")
                QMessageBox.warning(self, 'Wishlist Validation Error', f"Item {idx + 1}: Image is missing.")

        return not errors

    def clear_items(self):
        while self.items_layout.count():
            item = self.items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
