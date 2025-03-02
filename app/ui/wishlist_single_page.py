from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPen
from PyQt6.QtWidgets import *
from functools import partial


class WishSingleListPage(QFrame):
    def __init__(self, wish_item_service, name: str, parent, item_list):
        super().__init__(parent)
        self.wish_item_service = wish_item_service
        self.name = name
        self.item_list = item_list
        self.checkbox_list = []
        self.complete_ratio = QLabel()
        self.pending_updates = {}
        self.show_wishlist()

    def show_wishlist(self) -> None:

        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Sunken)

        wishlist_layout = QVBoxLayout(self)
        wishlist_layout.setSpacing(15)
        wishlist_layout.setContentsMargins(30, 10, 30, 10)
        wishlist_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        season_name_label = QLabel(f'Season {self.name}')
        season_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        season_name_label.setFont(QFont('Cambria math', 15))
        season_name_label.setMaximumHeight(30)

        self.complete_ratio.setFont(QFont('Cambria math', 15))
        self.complete_ratio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.complete_ratio.setMaximumHeight(30)

        wishlist_layout.addWidget(season_name_label)
        wishlist_layout.addWidget(self.complete_ratio)
        wishlist_layout.addSpacing(10)

        items_per_row = 8
        for row_idx in range(0, len(self.item_list), items_per_row):
            row_items = self.item_list[row_idx:row_idx + items_per_row]

            row_layout = QHBoxLayout()
            row_layout.setSpacing(20)
            row_layout.setContentsMargins(0, 0, 0, 0)

            row_layout.addStretch()

            for item in row_items:
                item_layout = QVBoxLayout()
                item_layout.setSpacing(5)
                item_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                item_name = QLabel(f'<b>{item.name}</b>')
                item_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

                image_label = QLabel()
                pixmap = QPixmap()
                pixmap.loadFromData(item.image_data)
                image_label.setPixmap(pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio))
                image_label.original_pixmap = image_label.pixmap()

                founded_layout = QHBoxLayout()
                founded_checkbox = QCheckBox()
                founded_checkbox.setChecked(item.founded)
                if founded_checkbox.isChecked():
                    self.mark_founded_item(image_label)
                founded_checkbox.stateChanged.connect(
                    partial(self.toggle_cross, founded_checkbox, image_label, item)
                )
                self.checkbox_list.append(founded_checkbox)
                founded_layout.addWidget(QLabel("<b>Found:</b>"))
                founded_layout.addWidget(founded_checkbox)
                founded_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                item_layout.addWidget(image_label)
                item_layout.addWidget(item_name)
                item_layout.addLayout(founded_layout)

                row_layout.addLayout(item_layout)

            row_layout.addStretch()
            wishlist_layout.addLayout(row_layout)

        self.complete_ratio.setText(f'Complete: {self.calculate_complete_ratio()}%')

    def save_pending_updates(self) -> None:
        if not self.pending_updates:
            return

        for _, item_data in self.pending_updates.items():
            item, founded_status = item_data
            item.founded = founded_status
            self.wish_item_service.update_wishlist_item(item)

        self.pending_updates.clear()

    def toggle_cross(self, checkbox, image_label, item) -> None:

        self.pending_updates[item.id] = (item, checkbox.isChecked())

        if checkbox.isChecked():
            self.mark_founded_item(image_label)
            self.update_complete_ratio()
        else:
            image_label.setPixmap(image_label.original_pixmap)
            self.update_complete_ratio()

    def calculate_complete_ratio(self) -> float:
        return 100 * sum(1 for cb in self.checkbox_list if cb.isChecked()) // len(
            self.checkbox_list) if self.checkbox_list else 0

    def update_complete_ratio(self) -> None:
        self.complete_ratio.setText(f'Complete: {self.calculate_complete_ratio()}%')


    @staticmethod
    def mark_founded_item(widget) -> None:
        pixmap = widget.pixmap().copy()
        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.GlobalColor.red, 2))

        width, height = pixmap.width(), pixmap.height()

        painter.drawLine(0, 0, width, height)
        painter.drawLine(width, 0, 0, height)

        painter.end()
        widget.setPixmap(pixmap)
