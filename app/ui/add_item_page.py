from image_dropout import PhotoDropout
from app.service.dto import CreateFinalItemDto
from PyQt6.QtCore import Qt, QRegularExpression
from app.utilities.button_style import main_button_style
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QTextEdit,
    QComboBox,
    QStyledItemDelegate,
)


class CenteredDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter
        super().paint(painter, option, index)


class AddItemPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.item_name = QLineEdit(self)
        self.description = QTextEdit(self)
        self.first_image = PhotoDropout()
        self.second_image = PhotoDropout()
        self.quantity = QLineEdit(self)
        self.finder_name = QLineEdit(self)
        self.locality_name = QLineEdit(self)
        self.location_name = QLineEdit(self)
        self.latitude = QLineEdit(self)
        self.longitude = QLineEdit(self)
        self.latitude_direction = QComboBox(self)
        self.longitude_direction = QComboBox(self)
        self.material_name = QLineEdit(self)
        self.epoch_name = QLineEdit(self)
        self.year = QLineEdit(self)
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(10)

        item_name_label = QLabel("Item Name:")
        description_name_label = QLabel("Description:")
        item_first_image_label = QLabel("First Image:")
        item_second_image_label = QLabel("Second Image:")
        quantity_label = QLabel("Quantity:")
        finder_name_label = QLabel("Name of finder:")
        locality_name_label = QLabel("Name of locality:")
        location_name_label = QLabel("Name of location:")
        latitude_label = QLabel("Latitude:")
        longitude_label = QLabel("Longitude:")
        latitude_direction_label = QLabel("Latitude direction:")
        longitude_direction_label = QLabel("Longitude direction:")
        material_label = QLabel("Name of material")
        epoch_label = QLabel("Name of epoch")
        year_label = QLabel("Year:")

        self.quantity.setValidator(QIntValidator(1, 10000))
        self.year.setValidator(QIntValidator(0, 2100))

        latitude_longitude_regex = QRegularExpression(r"^([0-9]{1, 3})(\.\d{1,2})?$")
        self.latitude.setValidator(
            QRegularExpressionValidator(latitude_longitude_regex, self)
        )
        self.longitude.setValidator(
            QRegularExpressionValidator(latitude_longitude_regex, self)
        )
        self.latitude_direction.addItems(["N", "S"])
        self.longitude_direction.addItems(["W", "E"])

        delegate_latitude = CenteredDelegate(self.latitude_direction)
        self.latitude_direction.setItemDelegate(delegate_latitude)
        delegate_longitude = CenteredDelegate(self.longitude_direction)
        self.longitude_direction.setItemDelegate(delegate_longitude)

        self.latitude_direction.setStyleSheet(
            """
            
            background-color: #ffd700;
            font-size: 14px;
            padding: 5px;
          
        """
        )
        self.longitude_direction.setStyleSheet(
            """
        
            background-color: #ffd700;
            font-size: 14px;
            padding: 5px;
        """
        )

        save_button = QPushButton("Save Item")
        save_button.setStyleSheet(main_button_style)
        save_button.clicked.connect(self.save_item)

        back_button = QPushButton("Back to Main Page")
        back_button.setStyleSheet(main_button_style)
        back_button.clicked.connect(self.go_to_start_window)

        layout.addWidget(item_name_label, 0, 0)
        layout.addWidget(self.item_name, 0, 1)
        layout.addWidget(description_name_label, 1, 0)
        layout.addWidget(self.description, 1, 1, 1, 2)
        layout.addWidget(item_first_image_label, 1, 4)
        layout.addWidget(self.first_image, 1, 5)
        layout.addWidget(item_second_image_label, 1, 6)
        layout.addWidget(self.second_image, 1, 7)
        layout.addWidget(quantity_label, 2, 0)
        layout.addWidget(self.quantity, 2, 1)
        layout.addWidget(finder_name_label, 3, 0)
        layout.addWidget(self.finder_name, 3, 1)
        layout.addWidget(locality_name_label, 4, 0)
        layout.addWidget(self.locality_name, 4, 1)
        layout.addWidget(location_name_label, 4, 2)
        layout.addWidget(self.location_name, 4, 3)
        layout.addWidget(latitude_label, 5, 0)
        layout.addWidget(self.latitude, 5, 1)
        layout.addWidget(latitude_direction_label, 5, 2)
        layout.addWidget(self.latitude_direction, 5, 3)
        layout.addWidget(longitude_label, 5, 4)
        layout.addWidget(self.longitude, 5, 5)
        layout.addWidget(longitude_direction_label, 5, 6)
        layout.addWidget(self.longitude_direction, 5, 7)
        layout.addWidget(material_label, 6, 0)
        layout.addWidget(self.material_name, 6, 1)
        layout.addWidget(epoch_label, 7, 0)
        layout.addWidget(self.epoch_name, 7, 1)
        layout.addWidget(year_label, 7, 2)
        layout.addWidget(self.year, 7, 3)

        layout.addWidget(save_button, 8, 0, 1, 8, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(back_button, 9, 0, 1, 8, Qt.AlignmentFlag.AlignCenter)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setColumnStretch(5, 1)
        layout.setColumnStretch(7, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(3, 1)

        layout.setRowMinimumHeight(0, 40)
        layout.setColumnMinimumWidth(1, 150)
        layout.setSpacing(10)
        self.setLayout(layout)

    def reset_style(self, widget):

        widget.setStyleSheet("")
        widget.setPlaceholderText("")

    def setup_signals(self):

        self.item_name.textChanged.connect(lambda x: self.reset_style(self.item_name))
        self.description.textChanged.connect(lambda: self.reset_style(self.description))
        self.quantity.textChanged.connect(lambda: self.reset_style(self.quantity))
        self.finder_name.textChanged.connect(lambda: self.reset_style(self.finder_name))
        self.locality_name.textChanged.connect(
            lambda: self.reset_style(self.locality_name)
        )
        self.latitude.textChanged.connect(lambda: self.reset_style(self.latitude))
        self.longitude.textChanged.connect(lambda: self.reset_style(self.longitude))
        self.material_name.textChanged.connect(
            lambda: self.reset_style(self.material_name)
        )
        self.epoch_name.textChanged.connect(lambda: self.reset_style(self.epoch_name))
        self.year.textChanged.connect(lambda: self.reset_style(self.year))

    def check_validation(self):
        self.setup_signals()
        errors = []

        def mark_invalid(widget, message):

            widget.setStyleSheet("color: #ff0000; border: 1px solid red;")
            widget.setPlaceholderText(message)
            errors.append(message)

        if not self.item_name.text():
            mark_invalid(self.item_name, "Name is required")

        if not self.description.toPlainText():
            mark_invalid(self.description, "Description is required")

        if not self.first_image.get_image() or not self.second_image.get_image():
            errors.append("Images are required")

        if not self.quantity.text():
            mark_invalid(self.quantity, "Quantity is required")
        else:
            try:
                quantity = int(self.quantity.text())
                if not (0 < quantity < 10000):
                    mark_invalid(self.quantity, "Quantity out of range")
            except ValueError:
                mark_invalid(self.quantity, "Quantity must be a number")

        if not self.finder_name.text():
            mark_invalid(self.finder_name, "Finder name is required")

        if not self.locality_name.text():
            mark_invalid(self.locality_name, "Locality name is required")

        if self.latitude.text():
            try:
                latitude = float(self.latitude.text())
                if not (0 <= latitude <= 90.0):
                    mark_invalid(self.latitude, "Latitude out of range")
            except ValueError:
                mark_invalid(self.latitude, "Latitude must be a number")

        if self.longitude.text():
            try:
                longitude = float(self.longitude.text())
                if not (0.0 <= longitude <= 180.0):
                    mark_invalid(self.longitude, "Longitude out of range")
            except ValueError:
                mark_invalid(self.longitude, "Longitude must be a number")

        if not self.material_name.text():
            mark_invalid(self.material_name, "Material name is required")

        if not self.epoch_name.text():
            mark_invalid(self.epoch_name, "Epoch name is required")

        if self.year.text():
            try:
                year = int(self.year.text())
                if not (0 <= year <= 2100):
                    mark_invalid(self.year, "Year is incorrect")
            except ValueError:
                mark_invalid(self.year, "Year must be a number")

        if errors:

            return False

        return True

    def save_item(self):

        if self.check_validation():

            item = CreateFinalItemDto(
                name=self.item_name.text(),
                description=self.description.toPlainText(),
                image_data=self.first_image.convert_to_bytes(),
                quantity=int(self.quantity.text()),
                finder_name=self.finder_name.text(),
                locality_name=self.locality_name.text(),
                location_name=self.location_name.text(),
                latitude=float(self.latitude.text()),
                longitude=float(self.longitude.text()),
                latitude_direction=self.latitude_direction.currentText(),
                longitude_direction=self.longitude_direction.currentText(),
                material_name=self.material_name.text(),
                epoch_name=self.epoch_name.text(),
                year=int(self.year.text()) if self.year.text() else None,
            )
            print(item)
            QMessageBox.information(self, "Submission correct", "Item saved correctly")

    def go_to_start_window(self):
        self.stacked_widget.setCurrentIndex(0)
