from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *
from app.utilities.button_style import main_button_style
from app.service.final_wish_item_service import FinalWishItemService
from app.ui.wishlist_single_page import WishSingleListPage

from functools import partial


class WishListPage(QWidget):
    def __init__(self, wish_item_service: FinalWishItemService, stacked_page: QStackedWidget):
        super().__init__()
        self.wish_item_service = wish_item_service
        self.stacked_page = stacked_page
        self.layout = QGridLayout(self)
        self.current_frame = None
        self.item_list = []
        self.checkbox_list = []
        self.wishlist_names = []
        self.wishlists = {}
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
        self.show_wishlist()

    def init_wishlist_left_bar(self) -> None:
        self.wishlist_names = self.wish_item_service.season_repository.get_all_seasons_name()

        for name in self.wishlist_names:
            if not self.wishlists.get(name):
                item_list = self.wish_item_service.wishlist_repository.get_items_where_value_equals(season_name=name)
                self.wishlists[name] = WishSingleListPage(
                    wish_item_service=self.wish_item_service,
                    name=name,
                    parent=self,
                    item_list=item_list
                )

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

            label.mousePressEvent = partial(self.on_wishlist_clicked, season)
            left_bar_layout.addWidget(label, Qt.AlignmentFlag.AlignHCenter)

        container = QWidget()
        container.setLayout(left_bar_layout)

        self.layout.addWidget(container, 2, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

    def on_wishlist_clicked(self, season_name: str, event) -> None:
        self.show_wishlist(season_name)

    def show_wishlist(self, season_name: str | None = None) -> None:
        if self.current_frame:
            self.layout.removeWidget(self.current_frame)
            self.current_frame.setParent(None)

        if self.wishlists.get(season_name):
            self.current_frame = self.wishlists[season_name]
        elif self.wishlist_names:
            self.current_frame = self.wishlists[self.wishlist_names[0]]

        self.layout.addWidget(self.current_frame, 2, 0, 3, 3, Qt.AlignmentFlag.AlignCenter)

    def on_close_event(self):
        for wishlist in self.wishlists.values():
            wishlist.save_pending_updates()

    def go_to_start_page(self) -> None:
        self.stacked_page.setCurrentIndex(0)

    def go_to_add_wishlist_page(self) -> None:
        self.stacked_page.setCurrentIndex(5)
