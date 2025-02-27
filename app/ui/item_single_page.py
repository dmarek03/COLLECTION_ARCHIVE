from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidgetItem,
    QTableWidget,
)
from app.utilities.button_style import main_button_style


class ItemSinglePage(QWidget):
    def __init__(self, item, stacked_widget):
        super().__init__()
        self.item = item
        self.stacked_widget = stacked_widget
        self.layout = QVBoxLayout(self)
        self.init_ui()

    def init_ui(self) -> None:

        first_image_label = QLabel()
        first_image_pixmap = QPixmap()
        first_image_pixmap.loadFromData(self.item.first_image_data)
        first_image_label.setPixmap(
            first_image_pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio)
        )

        first_image_frame = QFrame()
        first_image_frame.setFrameShape(QFrame.Shape.Box)
        first_image_frame.setLineWidth(2)
        first_image_layout = QVBoxLayout(first_image_frame)
        first_image_layout.addWidget(
            first_image_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        second_image_label = QLabel()
        second_image_pixmap = QPixmap()
        second_image_pixmap.loadFromData(self.item.second_image_data)
        second_image_label.setPixmap(
            second_image_pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio)
        )

        second_image_frame = QFrame()
        second_image_frame.setFrameShape(QFrame.Shape.Box)
        second_image_frame.setLineWidth(2)
        second_image_layout = QVBoxLayout(second_image_frame)
        second_image_layout.addWidget(
            second_image_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        image_layout = QHBoxLayout()
        image_layout.addWidget(first_image_frame)
        image_layout.addWidget(second_image_frame)
        image_layout.setSpacing(20)
        image_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lat_deg, lat_min, lat_sec = self.item.coordinates_to_dms(value=self.item.latitude)
        log_deg, log_min, log_sec = self.item.coordinates_to_dms(value=self.item.longitude)

        table_data = [
            ("Item name", self.item.name),
            ("Description", self.item.description),
            ("Quantity", self.item.quantity),
            ("Date of addition", self.item.addition_date),
            ("Date of finding", self.item.finding_date),
            ("Finder name", self.item.finder_name),
            ("Locality name", self.item.locality_name),
            ("Location name", self.item.location_name if self.item.location_name else "Indefinite"),
            (
                "Coordinates",
                f"{lat_deg}°{lat_min}′{lat_sec:.2f}″{self.item.latitude_direction},{log_deg}°{log_min}′{log_sec:.2f}″{self.item.longitude_direction}"
            ),
            ("Material name", self.item.material_name),
            ("Epoch name", self.item.epoch_name),
            ("Year", self.item.year if self.item.year else "Indefinite"),
        ]

        table_widget = QTableWidget(len(table_data), 2)
        table_widget.verticalHeader().setVisible(False)
        table_widget.horizontalHeader().setVisible(False)
        table_widget.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        table_widget.setSelectionMode(
            QTableWidget.SelectionMode.NoSelection
        )
        table_widget.setStyleSheet(
            "QTableWidget { border: 2px solid black;gridline-color: black;  }"
        )

        font_bold = QFont("Cambria Math", 13, QFont.Weight.DemiBold)

        for row, (field, value) in enumerate(table_data):
            field_item = QTableWidgetItem(field)
            field_item.setFont(font_bold)
            field_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table_widget.setItem(row, 0, field_item)

            value_label = QLabel(str(value))
            value_label.setWordWrap(True)
            description_text = value_label.text()
            wrapped_text = "\n".join(
                description_text[i: i + 50]
                for i in range(0, len(description_text), 50)
            )

            value_item = QTableWidgetItem(wrapped_text)
            value_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table_widget.setItem(row, 1, value_item)

        back_button = QPushButton("Back")
        back_button.setMaximumWidth(200)
        back_button.setStyleSheet(main_button_style)
        back_button.clicked.connect(self.back_to_collection_page)

        self.layout.addLayout(image_layout)
        self.layout.addWidget(table_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(20)

        self.setLayout(self.layout)

    def back_to_collection_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def showEvent(self, event):
        super().showEvent(event)
        self.adjust_table_size()

    def adjust_table_size(self):

        table_widget = self.findChild(QTableWidget)
        if table_widget:
            table_widget.resizeColumnsToContents()
            table_widget.resizeRowsToContents()

        total_width = table_widget.verticalHeader().width()
        for col in range(table_widget.columnCount()):
            total_width += table_widget.columnWidth(col)
        total_width += table_widget.frameWidth() * 2

        total_height = table_widget.horizontalHeader().height()
        for row in range(table_widget.rowCount()):
            total_height += table_widget.rowHeight(row)
        total_height += table_widget.frameWidth() * 2

        table_widget.setFixedWidth(total_width)
        table_widget.setFixedHeight(total_height)
