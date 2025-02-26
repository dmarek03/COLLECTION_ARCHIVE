from app.ui.image_dropout import PhotoDropout
from app.service.dto import CreateFinalItemDto
from PyQt6.QtCore import Qt, QRegularExpression, QDate
from app.utilities.button_style import main_button_style
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator, QPixmap
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QTextEdit,
    QDateEdit,
    QComboBox,
    QStyledItemDelegate,
)
from app.service.final_item_service import FinalItemService
from mysql.connector.pooling import Error


class CenteredDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter
        super().paint(painter, option, index)


class AddItemPage(QWidget):
    def __init__(self, item_service: FinalItemService, stacked_widget):
        super().__init__()
        self.item_service = item_service
        self.item_name = QLineEdit(self)
        self.description = QTextEdit(self)
        self.first_image = PhotoDropout()
        self.second_image = PhotoDropout()
        self.finding_date = QDateEdit(self)
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
        self.layout = QGridLayout(self)
        self.save_button = QPushButton("Save Item")
        self.save_updated_button = QPushButton('Save updated item')
        self.init_ui()

    def init_ui(self):
        self.layout.setSpacing(10)

        item_name_label = QLabel("Item Name:")
        description_name_label = QLabel("Description:")
        item_first_image_label = QLabel("First Image:")
        item_second_image_label = QLabel("Second Image:")
        finding_date_label = QLabel("Date of finding:")
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

        self.description.setMaximumHeight(400)
        self.description.setMaximumWidth(400)

        self.finding_date.setDate(QDate.currentDate())
        self.finding_date.setCalendarPopup(True)

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

        self.create_save_button()

        back_button = QPushButton("Back to Main Page")
        back_button.setStyleSheet(main_button_style)
        back_button.clicked.connect(self.go_to_start_window)

        self.layout.addWidget(item_name_label, 0, 0)
        self.layout.addWidget(self.item_name, 0, 1)
        self.layout.addWidget(description_name_label, 1, 0)
        self.layout.addWidget(self.description, 1, 1, 1, 2)
        self.layout.addWidget(item_first_image_label, 1, 4)
        self.layout.addWidget(self.first_image, 1, 5)
        self.layout.addWidget(item_second_image_label, 1, 6)
        self.layout.addWidget(self.second_image, 1, 7)
        self.layout.addWidget(finding_date_label, 2, 0)
        self.layout.addWidget(self.finding_date, 2, 1)
        self.layout.addWidget(quantity_label, 3, 0)
        self.layout.addWidget(self.quantity, 3, 1)
        self.layout.addWidget(finder_name_label, 4, 0)
        self.layout.addWidget(self.finder_name, 4, 1)
        self.layout.addWidget(locality_name_label, 5, 0)
        self.layout.addWidget(self.locality_name, 5, 1)
        self.layout.addWidget(location_name_label, 5, 2)
        self.layout.addWidget(self.location_name, 5, 3)
        self.layout.addWidget(latitude_label, 6, 0)
        self.layout.addWidget(self.latitude, 6, 1)
        self.layout.addWidget(latitude_direction_label, 6, 2)
        self.layout.addWidget(self.latitude_direction, 6, 3)
        self.layout.addWidget(longitude_label, 6, 4)
        self.layout.addWidget(self.longitude, 6, 5)
        self.layout.addWidget(longitude_direction_label, 6, 6)
        self.layout.addWidget(self.longitude_direction, 6, 7)
        self.layout.addWidget(material_label, 7, 0)
        self.layout.addWidget(self.material_name, 7, 1)
        self.layout.addWidget(epoch_label, 8, 0)
        self.layout.addWidget(self.epoch_name, 8, 1)
        self.layout.addWidget(year_label, 8, 2)
        self.layout.addWidget(self.year, 8, 3)

        self.layout.addWidget(back_button, 10, 0, 1, 8, Qt.AlignmentFlag.AlignCenter)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setColumnStretch(5, 1)
        self.layout.setColumnStretch(7, 1)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(3, 1)

        self.layout.setRowMinimumHeight(0, 40)
        self.layout.setColumnMinimumWidth(1, 150)
        self.layout.setColumnMinimumWidth(3, 150)
        self.layout.setColumnMinimumWidth(5, 200)
        self.layout.setColumnMinimumWidth(7, 200)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

    @staticmethod
    def reset_style(widget):

        widget.setStyleSheet("")
        widget.setPlaceholderText("")

    def reset_fields(self) -> None:
        self.item_name.clear()
        self.description.clear()
        self.first_image.clear()
        self.second_image.clear()
        self.finding_date.setDate(QDate.currentDate())
        self.quantity.clear()
        self.finder_name.clear()
        self.locality_name.clear()
        self.location_name.clear()
        self.latitude.clear()
        self.longitude.clear()
        self.latitude_direction.setCurrentIndex(0)
        self.longitude_direction.setCurrentIndex(0)
        self.material_name.clear()
        self.epoch_name.clear()
        self.year.clear()

    def set_fields(self, item: CreateFinalItemDto) -> None:

        pixmap1 = QPixmap()
        pixmap1.loadFromData(item.first_image_data)

        pixmap2 = QPixmap()
        pixmap2.loadFromData(item.second_image_data)

        self.item_name.setText(item.name)
        self.description.setText(item.description)
        self.first_image.photo.setPixmap(pixmap1)
        self.second_image.photo.setPixmap(pixmap2)
        self.finding_date.setDate(item.finding_date)
        self.quantity.setText(str(item.quantity))
        self.finder_name.setText(item.finder_name)
        self.locality_name.setText(item.locality_name)
        self.location_name.setText(item.location_name)
        self.latitude.setText(str(item.latitude))
        self.longitude.setText(str(item.longitude))
        self.latitude_direction.setCurrentText(item.latitude_direction)
        self.longitude_direction.setCurrentText(item.longitude_direction)
        self.material_name.setText(item.material_name)
        self.epoch_name.setText(item.epoch_name)
        self.year.setText(str(item.year)) if item.year else ''

    def setup_signals(self):

        self.item_name.textChanged.connect(lambda: self.reset_style(self.item_name))
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
            QMessageBox.warning(self, 'Lack of item images', 'Images are required')

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

    def create_item_from_data(self) -> CreateFinalItemDto:
        return CreateFinalItemDto(
            name=self.item_name.text().strip(),
            description=self.description.toPlainText(),
            first_image_data=self.first_image.convert_to_bytes(),
            second_image_data=self.second_image.convert_to_bytes(),
            finding_date=self.finding_date.date().toString("yyyy-MM-dd"),
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

    def create_save_button(self) -> None:
        self.save_button = QPushButton('Save')
        self.save_button.setStyleSheet(main_button_style)
        self.save_button.clicked.connect(self.save_item)
        self.layout.addWidget(self.save_button, 9, 0, 1, 8, Qt.AlignmentFlag.AlignCenter)

    def create_save_updated_button(self, item: CreateFinalItemDto) -> None:
        self.save_updated_button = QPushButton('Save updated item')
        self.save_updated_button.setStyleSheet(main_button_style)
        self.save_updated_button.clicked.connect(lambda _, w=item: self.update_item(w))
        self.layout.addWidget(self.save_updated_button, 9, 0, 1, 8, Qt.AlignmentFlag.AlignCenter)

    def go_to_edition_page(self, item: CreateFinalItemDto) -> None:

        self.layout.removeWidget(self.save_button)
        self.save_button.deleteLater()

        self.create_save_updated_button(item)
        self.set_fields(item)

    def update_item(self, item: CreateFinalItemDto) -> None:

        if self.check_validation():

            updated_item = self.create_item_from_data()
            try:
                print(f'Add item page :{item.id=}')
                self.item_service.update_final_item(old_item_id=item.id, updated_item=updated_item)

            except Error as err:
                QMessageBox.warning(self, 'Submission incorrect', err.msg)

            finally:
                QMessageBox.information(
                    self, "Submission correct", "Item updated correctly"
                )
                collection_page = self.stacked_widget.widget(1)
                collection_page.create_single_pages()
                collection_page.init_filter_bar()

                collection_page = self.stacked_widget.widget(1)
                collection_page.create_single_pages()
                collection_page.init_filter_bar()

                self.reset_fields()
                self.layout.removeWidget(self.save_updated_button)
                self.save_updated_button.deleteLater()
                self.create_save_button()

    def save_item(self):

        if self.check_validation():

            item = self.create_item_from_data()

            try:
                self.item_service.add_final_item(create_final_item_dto=item)

            except Error as err:
                QMessageBox.warning(self, "Submission incorrect", err.msg)

            finally:
                QMessageBox.information(
                    self, "Submission correct", "Item saved correctly"
                )
                self.reset_fields()

    def go_to_start_window(self):
        self.stacked_widget.setCurrentIndex(0)
