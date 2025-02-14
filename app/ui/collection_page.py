from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton
from app.utilities.button_style import main_button_style


class CollectionPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        # Nagłówek
        label = QLabel("Collection Page")
        label_font = QFont("Cambria Math", 30, QFont.Weight.Bold)
        label.setFont(label_font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Przycisk powrotu
        start_window_button = QPushButton("Back to Start Page")
        start_window_button.setMaximumWidth(200)
        start_window_button.setStyleSheet(main_button_style)
        start_window_button.clicked.connect(self.go_to_start_window)

        # Układ w siatce
        layout.addWidget(label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(start_window_button, 1, 0, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def go_to_start_window(self):
        self.stacked_widget.setCurrentIndex(0)
