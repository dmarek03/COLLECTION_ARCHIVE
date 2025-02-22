import math
from typing import Any
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QStackedWidget, QLineEdit, QHBoxLayout, \
    QComboBox, QVBoxLayout, QDateEdit, QFrame, QCheckBox, QMessageBox
from app.utilities.button_style import main_button_style
from app.ui.collection_single_page import CollectionSinglePage
from app.utilities.column_names_dict import item_attributes_to_db_column_mapping
from app.service.final_item_service import FinalItemService


class CollectionPage(QWidget):
    def __init__(self, item_service: FinalItemService, stacked_widget: QStackedWidget):
        super().__init__()
        self.item_service = item_service
        self.stacked_widget = stacked_widget
        self.page_count = 0
        self.current_page_idx = 0
        self.stacked_collection_page = QStackedWidget(self)
        self.layout = QGridLayout(self)
        self.input_search = None
        self.sort_dropdown = None
        self.sorting_order = None
        self.filter_bar_layout = QVBoxLayout(self)
        self.init_ui()
        self.init_tool_bar()
        self.init_filter_bar()

    def init_ui(self):
        label = QLabel("Collection Page")
        label_font = QFont("Cambria Math", 30, QFont.Weight.Bold)
        label.setFont(label_font)
        label.setMaximumHeight(100)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        item_list = self.item_service.founded_items_repository.get_all_items_order_by(value=None, descending=False)
        print(f'{item_list=}')
        self.page_count = math.ceil(len(item_list) / 5)
        for i in range(len(item_list)):
            single_collection_page = CollectionSinglePage(self.item_service, self.stacked_widget, i, item_list[i*5:(i+1)*5])
            self.stacked_collection_page.addWidget(single_collection_page)

        start_window_button = QPushButton("Back to Start Page")
        start_window_button.setMaximumWidth(200)
        start_window_button.setStyleSheet(main_button_style)
        start_window_button.clicked.connect(self.go_to_start_window)

        next_page_button = QPushButton('Next page')
        next_page_button.setMaximumWidth(200)
        next_page_button.setStyleSheet(main_button_style)
        next_page_button.clicked.connect(self.go_to_next_page)

        previous_page_button = QPushButton('Previous page')
        previous_page_button.setMaximumWidth(200)
        previous_page_button.setStyleSheet(main_button_style)
        previous_page_button.clicked.connect(self.go_to_previous_page)

        self.layout.addWidget(label, 0, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.stacked_collection_page, 2, 1, 2, 3)
        self.layout.addWidget(previous_page_button, 4, 1, Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(start_window_button, 4, 2, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(next_page_button, 4, 3, Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.layout)

    def init_tool_bar(self):

        tool_bar_layout = QHBoxLayout()

        self.input_search = QLineEdit(self)
        self.input_search.setPlaceholderText("What are you looking for?")
        self.input_search.setFixedHeight(30)

        search_button = QPushButton("Search")
        search_button.setFixedHeight(30)
        search_button.clicked.connect(lambda: self.search(self.input_search.text()))

        sort_label = QLabel('Sort by:')
        sort_label.setMaximumHeight(30)
        order_label = QLabel('Order:')
        order_label.setMaximumHeight(30)

        self.sort_dropdown = QComboBox()
        self.sort_dropdown.addItems([
            "Default", "Name", "Finding date", "Addition date", "Quantity",
            "Finder name", "Locality name", "Location name", "Material name", "Year"
        ])
        self.sort_dropdown.setFixedHeight(30)
        self.sorting_order = QComboBox()
        self.sorting_order.addItems(['Ascending', 'Descending'])
        self.sorting_order.setMaximumHeight(30)

        tool_bar_layout.addWidget(self.input_search)
        tool_bar_layout.addWidget(sort_label)
        tool_bar_layout.addWidget(self.sort_dropdown)
        tool_bar_layout.addWidget(order_label)
        tool_bar_layout.addWidget(self.sorting_order)
        tool_bar_layout.addWidget(search_button)

        self.layout.addLayout(tool_bar_layout, 1, 1, 1, 3)

    def init_filter_bar(self) -> None:

        self.filter_bar_layout.setSpacing(10)
        self.filter_bar_layout.setContentsMargins(5, 5, 5, 5)

        filter_label = QLabel("Filters")
        filter_label.setFont(QFont("Cambria Math", 16, QFont.Weight.Bold))
        filter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        filter_label.setMaximumWidth(350)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setFixedHeight(2)
        separator.setMaximumWidth(350)

        quantity_label = QLabel('Quantity')
        quantity_label.setMaximumWidth(250)
        quantity_label.setFont(QFont("Cambria Math", 12, QFont.Weight.Bold))

        quantity_validator = QIntValidator()
        quantity_validator.setRange(0, 1000)
        quantity_min_range = QLineEdit(self)
        quantity_min_range.setValidator(quantity_validator)
        quantity_min_range.setPlaceholderText('from')
        quantity_min_range.setMaximumWidth(150)

        quantity_max_range = QLineEdit(self)
        quantity_max_range.setValidator(quantity_validator)
        quantity_max_range.setPlaceholderText('to')
        quantity_max_range.setMaximumWidth(150)

        finding_date_label = QLabel('Finding date')
        finding_date_label.setMaximumWidth(250)
        finding_date_label.setFont(QFont("Cambria Math", 12, QFont.Weight.Bold))

        finding_date_min = QDateEdit()
        finding_date_min.setDate(QDate.currentDate())
        finding_date_min.setCalendarPopup(True)
        finding_date_min.setMaximumWidth(250)

        finding_date_max = QDateEdit()
        finding_date_max.setDate(QDate.currentDate())
        finding_date_max.setCalendarPopup(True)
        finding_date_max.setMaximumWidth(250)

        year_label = QLabel('Year')
        year_label.setMaximumWidth(250)
        year_label.setFont(QFont("Cambria Math", 12, QFont.Weight.Bold))

        year_validator = QIntValidator()
        year_validator.setRange(0, 1000)
        year_min_range = QLineEdit(self)
        year_min_range.setValidator(year_validator)
        year_min_range.setPlaceholderText('from')
        year_min_range.setMaximumWidth(150)

        year_max_range = QLineEdit(self)
        year_max_range.setValidator(year_validator)
        year_max_range.setPlaceholderText('to')
        year_max_range.setMaximumWidth(150)

        filters = {
            "Finder name": QLineEdit(),
            "Locality name": QLineEdit(),
            "Location name": QLineEdit(),
            "Material name": QLineEdit(),
            "Epoch name": QLineEdit(),
        }

        quantity_layout = QVBoxLayout()
        quantity_layout.addWidget(quantity_label)
        quantity_layout.addWidget(quantity_min_range)
        quantity_layout.addWidget(quantity_max_range)

        self.filter_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.filter_bar_layout.addWidget(filter_label)
        self.filter_bar_layout.addWidget(separator)
        self.filter_bar_layout.addWidget(quantity_label)
        self.filter_bar_layout.addWidget(quantity_min_range)
        self.filter_bar_layout.addWidget(quantity_max_range)
        self.filter_bar_layout.addWidget(finding_date_label)
        self.filter_bar_layout.addWidget(finding_date_min)
        self.filter_bar_layout.addWidget(finding_date_max)
        self.filter_bar_layout.addWidget(year_label)
        self.filter_bar_layout.addWidget(year_min_range)
        self.filter_bar_layout.addWidget(year_max_range)

        for label, widget in filters.items():
            widget.setMaximumWidth(250)
            widget.setPlaceholderText(f'Enter {label}')
            widget_label = QLabel(label)
            widget_label.setMaximumWidth(250)
            widget_label.setFont(QFont("Cambria Math", 12, QFont.Weight.Bold))

            self.filter_bar_layout.addWidget(widget_label)
            self.filter_bar_layout.addWidget(widget)
            if options := self.filter_options(label):
                for i in range(0, len(options), 2):
                    op_layout = QHBoxLayout(self)
                    op_layout.setSpacing(10)
                    op_layout.addWidget(options[i])
                    op_layout.addWidget(options[i + 1])
                    self.filter_bar_layout.addLayout(op_layout)

        filter_button = QPushButton('Filter')
        filter_button.setStyleSheet(main_button_style)
        filter_button.setMaximumWidth(100)
        filter_button.setMaximumHeight(60)
        filter_button.clicked.connect(self.filter)

        self.filter_bar_layout.addWidget(filter_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addLayout(self.filter_bar_layout, 1, 0, 3, 1)

    def go_to_start_window(self):
        self.stacked_widget.setCurrentIndex(0)

    def search(self, item_name: str) -> None:
        print(f'Searching item {item_name}')
        sorting_column_name = item_attributes_to_db_column_mapping[self.sort_dropdown.currentText()]
        sorting_order = self.sorting_order.currentText()
        print(f'{sorting_column_name=}')
        print(f'{sorting_order=}')

    def filter(self) -> None:
        print(f'Filtering')
        self.get_filters_values()

    def go_to_next_page(self):
        if self.current_page_idx < self.page_count - 1:
            self.current_page_idx += 1
            self.stacked_collection_page.setCurrentIndex(self.current_page_idx)

    def go_to_previous_page(self):
        if self.current_page_idx > 0:
            self.current_page_idx -= 1
            self.stacked_collection_page.setCurrentIndex(self.current_page_idx)

    def filter_options(self, category_name: str):

        if category_name == 'Finder name':
            return [QCheckBox('Dominik'), QCheckBox('Adam')]

        if category_name == 'Material name':
            return [QCheckBox('silver'), QCheckBox('bronze'), QCheckBox('gold'), QCheckBox('copper')]

    @staticmethod
    def reset_style(widget):

        widget.setStyleSheet("")
        widget.setPlaceholderText("")

    def validate_filters(self) -> bool:
        errors = []

        def mark_invalid(widget, message):
            widget.setStyleSheet("color: #ff0000; border: 1px solid red;")
            widget.setPlaceholderText(message)
            errors.append(message)

        i = 0
        while i < self.filter_bar_layout.count():
            item = self.filter_bar_layout.itemAt(i)

            if item is None:
                i += 1
                continue

            widget = item.widget()

            if isinstance(widget, QLabel) and widget.text() in ['Quantity', 'Finding date', 'Year']:
                r_min = self.filter_bar_layout.itemAt(
                    i + 1).widget() if i + 1 < self.filter_bar_layout.count() else None
                r_max = self.filter_bar_layout.itemAt(
                    i + 2).widget() if i + 2 < self.filter_bar_layout.count() else None

                if r_min and r_max:

                    if isinstance(r_min, QLineEdit):
                        r_min.textChanged.connect(lambda _, w=r_min: self.reset_style(w))
                        r_max.textChanged.connect(lambda _, w=r_max: self.reset_style(w))

                        min_val = r_min.text()
                        max_val = r_max.text()

                        if max_val and not min_val:
                            mark_invalid(r_min, f'Low {widget.text()} range limit is required')
                        elif min_val and not max_val:
                            mark_invalid(r_max, f'Upper {widget.text()} range limit is required')
                        elif min_val and max_val:
                            try:
                                if int(min_val) > int(max_val):
                                    r_min.setText('')
                                    r_max.setText('')
                                    mark_invalid(r_min, f'Range is incorrect')
                                    mark_invalid(r_max, f'Range is incorrect')
                            except ValueError:
                                mark_invalid(r_min, f'Invalid number')
                                mark_invalid(r_max, f'Invalid number')

                    elif isinstance(r_min, QDateEdit):

                        min_date = r_min.date().toString("yyyy-MM-dd")
                        max_date = r_max.date().toString("yyyy-MM-dd")

                        if min_date > max_date:
                            QMessageBox.warning(
                                self,
                                "Incorrect finding date range",
                                "Lower date should be earlier than upper one"
                            )

                            errors.append('Incorrect year range')

                i += 2
            i += 1

        return not errors

    def get_filters_values(self) -> tuple[dict[str, Any], dict[str, tuple[Any, Any]]]:
        if self.validate_filters():
            single_value_filters = {}
            range_filters = {}

            i = 0
            name = None
            checkboxes = {}

            while i < self.filter_bar_layout.count():
                item = self.filter_bar_layout.itemAt(i)

                if item is None:
                    i += 1
                    continue

                widget = item.widget()

                if widget and isinstance(widget, QLabel):
                    name = widget.text()

                elif widget and isinstance(widget, QLineEdit) and widget.text():
                    if name in ['Quantity', 'Year']:
                        min_widget = widget
                        max_widget = self.filter_bar_layout.itemAt(i + 1).widget()

                        if max_widget and isinstance(max_widget, QLineEdit):
                            min_value = min_widget.text()
                            max_value = max_widget.text()
                            if name:
                                range_filters[item_attributes_to_db_column_mapping[name]] = (min_value, max_value)
                            i += 1
                    else:
                        if name and widget.text():
                            single_value_filters[item_attributes_to_db_column_mapping[name]] = [widget.text()]

                elif widget and isinstance(widget, QDateEdit):
                    min_widget = widget
                    max_widget = self.filter_bar_layout.itemAt(i + 1).widget()

                    if max_widget and isinstance(max_widget, QDateEdit):
                        min_date = min_widget.date().toString("yyyy-MM-dd")
                        max_date = max_widget.date().toString("yyyy-MM-dd")
                        if name:
                            range_filters[item_attributes_to_db_column_mapping[name]] = (min_date, max_date)
                        i += 1
                elif isinstance(item, QHBoxLayout):
                    for j in range(item.count()):
                        sub_widget = item.itemAt(j).widget()
                        if isinstance(sub_widget, QCheckBox) and sub_widget.isChecked():
                            if name and name not in checkboxes:
                                checkboxes[name] = []
                            checkboxes[name].append(sub_widget.text())

                i += 1
            for key, values in checkboxes.items():
                single_value_filters[item_attributes_to_db_column_mapping[key]] = values

            for key, values in single_value_filters.items():
                single_value_filters[key] = tuple(values) if len(values) > 1 else f"('{values[0]}')"

            print(f'{single_value_filters=}')
            print(f'{range_filters=}')

            return single_value_filters, range_filters
