from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QColor
from app.ui.collection_page import CollectionPage
from app.ui.add_item_page import AddItemPage
from app.ui.settings_page import SettingPage
from app.ui.wishlist_page import WishListPage
from app.ui.add_wishlist_items_page import AddWishlistItemsPage
from app.utilities.button_style import main_button_style
from app.service.final_item_service import FinalItemService
from app.service.final_wish_item_service import FinalWishItemService


class StartPage(QMainWindow):
    def __init__(self, item_service: FinalItemService, wish_item_service: FinalWishItemService) -> None:
        super().__init__()
        self.item_service = item_service
        self.wish_item_service = wish_item_service

        self.setWindowTitle("Collection Archive")
        self.setGeometry(100, 100, 500, 500)

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.main_widget = self.create_main_widget()
        self.stacked_widget.addWidget(self.main_widget)

        my_collection_window = CollectionPage(self.item_service, self.stacked_widget)
        add_item_window = AddItemPage(self.item_service, self.stacked_widget)
        settings_page = SettingPage(self.stacked_widget)
        wishlist_page = WishListPage(self.wish_item_service, self.stacked_widget)
        add_wishlist_page = AddWishlistItemsPage(self.wish_item_service, self.stacked_widget)

        self.stacked_widget.addWidget(my_collection_window)
        self.stacked_widget.addWidget(add_item_window)
        self.stacked_widget.addWidget(settings_page)
        self.stacked_widget.addWidget(wishlist_page)
        self.stacked_widget.addWidget(add_wishlist_page)
        self.stacked_widget.setStyleSheet("background-color: #daa520;")

        image_path = "ui/main_background.png"

        self.main_widget.setStyleSheet(
            f"background-image: url('{image_path}'); "
            f"background-position: center; "
            f"background-size: cover;"
        )

        self.show()

    def create_main_widget(self):
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setSpacing(20)

        label = QLabel("Collection Archive")
        label_font = QFont("Cambria Math", 30, QFont.Weight.Bold)
        label.setFont(label_font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        glow_effect = QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QColor(255, 223, 0, 180))
        glow_effect.setOffset(0, 0)

        label.setGraphicsEffect(glow_effect)

        my_collection_button = QPushButton("My Collection")
        my_collection_button.setMaximumWidth(200)
        my_collection_button.setStyleSheet(main_button_style)
        my_collection_button.clicked.connect(self.go_to_my_collection_window)

        add_item_button = QPushButton("Add Item")
        add_item_button.setMaximumWidth(200)
        add_item_button.setStyleSheet(main_button_style)
        add_item_button.clicked.connect(self.go_to_add_item_window)

        settings_button = QPushButton("Settings")
        settings_button.setMaximumWidth(200)
        settings_button.setStyleSheet(main_button_style)
        settings_button.clicked.connect(self.go_to_settings_page)

        wishlist_button = QPushButton('My Wishlist')
        wishlist_button.setMaximumWidth(200)
        wishlist_button.setStyleSheet(main_button_style)
        wishlist_button.clicked.connect(self.go_to_wishlist_page)

        layout.addWidget(label, 0, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(my_collection_button, 1, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(settings_button, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(wishlist_button, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(add_item_button, 1, 3, Qt.AlignmentFlag.AlignCenter)

        return widget

    def go_to_my_collection_window(self) -> None:
        self.stacked_widget.setCurrentIndex(1)

    def go_to_add_item_window(self) -> None:
        self.stacked_widget.setCurrentIndex(2)

    def go_to_settings_page(self) -> None:
        self.stacked_widget.setCurrentIndex(3)

    def go_to_wishlist_page(self) -> None:
        self.stacked_widget.setCurrentIndex(4)
