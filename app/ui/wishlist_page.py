import sys
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPen
from PyQt6.QtWidgets import *
from app.utilities.button_style import main_button_style
from app.service.final_wish_item_service import FinalWishItemService
from functools import partial


class WishListPage(QWidget):
    def __init__(self, wish_item_service: FinalWishItemService, stacked_page: QStackedWidget):
        super().__init__()
        self.wish_item_service = wish_item_service
        self.stacked_page = stacked_page
        self.layout = QGridLayout(self)
        self.frame_layout = None
        self.current_frame = QFrame(self)
        self.item_list = []
        self.checkbox_list = []
        self.wishlist_names = []
        self.init_ui()

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

        self.layout.addWidget(name_label, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(back_button, 5, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(create_wishlist_button, 5, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.init_wishlist_left_bar()
        self.show_wishlist(season_name=self.wishlist_names[0])

    def init_wishlist_left_bar(self) -> None:
        self.wishlist_names = self.wish_item_service.season_repository.get_all_seasons_name()

        left_bar_layout = QVBoxLayout()
        left_bar_layout.setSpacing(10)
        left_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_label = QLabel("My Wishlists")
        title_label.setMaximumHeight(30)
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        left_bar_layout.addWidget(title_label)

        for season in self.wishlist_names:
            label = QLabel(season)
            label.setMaximumHeight(30)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.setStyleSheet("""
                    font-size: 14px;
                    color: blue;
                    text-decoration: underline;
                    margin-left: 20px;

                """)

            label.mousePressEvent = lambda _, w=season: self.show_wishlist(season_name=w)
            left_bar_layout.addWidget(label, Qt.AlignmentFlag.AlignHCenter)

        container = QWidget()
        container.setLayout(left_bar_layout)

        self.layout.addWidget(container, 2, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

    def show_wishlist(self, season_name: str | None = None) -> None:
        if self.current_frame:
            self.layout.removeWidget(self.current_frame)
            self.current_frame.deleteLater()
            self.current_frame = None

        self.checkbox_list.clear()
        self.item_list = self.wish_item_service.wishlist_repository.get_items_where_value_equals(
            season_name=season_name)

        self.current_frame = QFrame(self)
        self.current_frame.setFrameShape(QFrame.Shape.Box)
        self.current_frame.setFrameShadow(QFrame.Shadow.Sunken)

        wishlist_layout = QVBoxLayout(self.current_frame)
        wishlist_layout.setSpacing(15)
        wishlist_layout.setContentsMargins(30, 10, 30, 10)
        wishlist_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        season_name_label = QLabel(f'Season {season_name}')
        season_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        season_name_label.setFont(QFont('Cambria math', 15))
        season_name_label.setMaximumHeight(30)

        self.complete_ratio = QLabel(f'Complete: {self.calculate_complete_ratio()}%')
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
                founded_checkbox.stateChanged.connect(partial(self.toggle_cross, founded_checkbox, image_label))
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

        self.layout.addWidget(self.current_frame, 2, 0, 3, 3, Qt.AlignmentFlag.AlignCenter)

    def toggle_cross(self, checkbox, image_label) -> None:
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

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                print(widget)
                widget.deleteLater()
            else:
                print(item)
                self.clear_layout(item.layout())

    def go_to_start_page(self) -> None:
        self.stacked_page.setCurrentIndex(0)

    def go_to_add_wishlist_page(self) -> None:
        self.stacked_page.setCurrentIndex(5)
