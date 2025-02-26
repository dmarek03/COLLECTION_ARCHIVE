
import math
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QGridLayout, QSpinBox, QStackedWidget
)
from app.ui.image_dropout import PhotoDropout
from app.utilities.button_style import main_button_style


class AddWishlistItemsPage(QWidget):
    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.items_container = QWidget()
        self.items_layout = QVBoxLayout()
        self.items_container.setLayout(self.items_layout)
        self.item_count_selector = QSpinBox()
        self.add_items_button = QPushButton('Add Items')
        self.create_wish_list_button = QPushButton('Create Wish List')
        self.init_ui()

    def init_ui(self) -> None:
        page_label = QLabel('Create Wish List')
        page_label.setFont(QFont("Cambria Math", 30))
        page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        selection_layout = QHBoxLayout()
        selection_layout.setSpacing(10)
        item_count_label = QLabel('Select number of items:')
        item_count_label.setFont(QFont("Cambria Math", 15))
        item_count_label.setMaximumWidth(300)

        self.item_count_selector.setRange(5, 20)
        self.item_count_selector.setValue(10)
        self.item_count_selector.setMaximumWidth(200)

        selection_layout.addWidget(item_count_label, Qt.AlignmentFlag.AlignLeft)
        selection_layout.addWidget(self.item_count_selector, Qt.AlignmentFlag.AlignLeft)

        self.add_items_button.setStyleSheet(main_button_style)
        self.add_items_button.setMaximumWidth(200)
        self.add_items_button.clicked.connect(self.add_items)

        self.create_wish_list_button.setStyleSheet(main_button_style)
        self.create_wish_list_button.setMaximumWidth(200)
        self.create_wish_list_button.setVisible(False)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_items_button, Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.create_wish_list_button, Qt.AlignmentFlag.AlignCenter)


        self.layout.addWidget(page_label, Qt.AlignmentFlag.AlignHCenter)
        self.layout.addLayout(selection_layout, Qt.AlignmentFlag.AlignHCenter)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.items_container, Qt.AlignmentFlag.AlignHCenter)


    def add_items(self) -> None:
        self.items_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.items_layout.setSpacing(10)

        items_count = self.item_count_selector.value()
        row_num = math.ceil(items_count / 5)

        for i in range(row_num):
            row_layout = QHBoxLayout()
            for _ in range(min(5, items_count)):
                widget = QWidget()
                widget.setMaximumWidth(200)
                widget.setMaximumHeight(200)

                item_layout = QGridLayout()
                item_layout.setSpacing(10)

                image_label = QLabel('Select image:')
                image = PhotoDropout()
                image.self_set_size(w_size=180, h_size=180)
                name_label = QLabel("Item name:")
                item_name = QLineEdit()

                item_layout.addWidget(image_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
                item_layout.addWidget(image, 0, 1, Qt.AlignmentFlag.AlignCenter)
                item_layout.addWidget(name_label, 1, 0, Qt.AlignmentFlag.AlignCenter)
                item_layout.addWidget(item_name, 1, 1, Qt.AlignmentFlag.AlignCenter)

                widget.setLayout(item_layout)
                row_layout.addWidget(widget)

                items_count -= 1
                if items_count <= 0:
                    break

            self.items_layout.addLayout(row_layout)

        self.add_items_button.setVisible(False)
        self.create_wish_list_button.setVisible(True)

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
