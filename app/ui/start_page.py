import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import *
from collection_page import CollectionPage
from add_item_page import AddItemPage
from app.utilities.button_style import main_button_style


class StartPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Collection Archive")
        self.setGeometry(100, 100, 500, 500)

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.main_widget = self.create_main_widget()
        self.stacked_widget.addWidget(self.main_widget)

        my_collection_window = CollectionPage(self.stacked_widget, 5)
        add_item_window = AddItemPage(self.stacked_widget)

        self.stacked_widget.addWidget(my_collection_window)
        self.stacked_widget.addWidget(add_item_window)
        self.stacked_widget.setStyleSheet("background-color: #daa520;")

        self.main_widget.setStyleSheet(
            """
                        background-image: url('main_background.png');
                        background-position: center;
                        background-size: cover; /* Dopasowanie obrazu do rozmiaru okna */
                """
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
        add_item_button = QPushButton("Add Item")

        my_collection_button.setMaximumWidth(200)
        add_item_button.setMaximumWidth(200)

        my_collection_button.clicked.connect(self.go_to_my_collection_window)
        add_item_button.clicked.connect(self.go_to_add_item_window)

        my_collection_button.setStyleSheet(main_button_style)

        add_item_button.setStyleSheet(main_button_style)

        layout.addWidget(label, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(my_collection_button, 1, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(add_item_button, 1, 1, Qt.AlignmentFlag.AlignCenter)

        return widget

    def go_to_my_collection_window(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_add_item_window(self):
        self.stacked_widget.setCurrentIndex(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartPage()
    window.show()
    sys.exit(app.exec())
