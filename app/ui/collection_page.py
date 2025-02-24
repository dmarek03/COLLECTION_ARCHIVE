import math
from typing import Any
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QLineEdit,
    QHBoxLayout,
    QComboBox,
    QVBoxLayout,
    QDateEdit,
    QFrame,
    QCheckBox,
    QMessageBox,
)
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
        self.number_of_items_on_page = 5
        self.stacked_collection_page = QStackedWidget(self)
        self.layout = QGridLayout(self)
        self.input_search = QLineEdit(self)
        self.sort_dropdown = QComboBox()
        self.sorting_order = QComboBox()
        self.filter_bar_layout = QVBoxLayout(self)
        self.item_not_found_layout = None
        self.init_ui()
        self.init_tool_bar()
        self.init_filter_bar()

    def init_ui(self):

        label = QLabel("Collection Page")
        label_font = QFont("Cambria Math", 30, QFont.Weight.Bold)
        label.setFont(label_font)
        label.setMaximumHeight(100)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.create_single_pages()

        start_window_button = QPushButton("Back to Start Page")
        start_window_button.setMaximumWidth(200)
        start_window_button.setStyleSheet(main_button_style)
        start_window_button.clicked.connect(self.go_to_start_window)

        next_page_button = QPushButton("Next page")
        next_page_button.setMaximumWidth(200)
        next_page_button.setStyleSheet(main_button_style)
        next_page_button.clicked.connect(self.go_to_next_page)

        previous_page_button = QPushButton("Previous page")
        previous_page_button.setMaximumWidth(200)
        previous_page_button.setStyleSheet(main_button_style)
        previous_page_button.clicked.connect(self.go_to_previous_page)

        self.layout.addWidget(label, 0, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.stacked_collection_page, 2, 1, 2, 3)
        self.layout.addWidget(previous_page_button, 4, 1, Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(start_window_button, 4, 2, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(next_page_button, 4, 3, Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.layout)

    def create_single_pages(
        self, item_list: list = None, is_searching: bool = False
    ) -> None:

        if self.item_not_found_layout:
            self.clear_layout(self.item_not_found_layout)
            self.layout.removeItem(self.item_not_found_layout)

        if not (is_searching or item_list):

            order = self.sorting_order.currentData()
            item_list = (
                self.item_service.founded_items_repository.get_all_items_order_by(
                    value=None, descending=order
                )
            )

        elif is_searching and not item_list:
            self.item_not_found_layout = QVBoxLayout()
            label = QLabel("Items not found")
            label.setMaximumHeight(100)
            label.setMaximumWidth(300)
            label.setFont(QFont("Cambria Math", 16, QFont.Weight.Bold))
            self.item_not_found_layout.addWidget(label, Qt.AlignmentFlag.AlignCenter)
            self.layout.addLayout(
                self.item_not_found_layout, 2, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter
            )

        new_page_count = math.ceil(len(item_list) / self.number_of_items_on_page)
        for i in range(self.stacked_collection_page.count()):
            single_page = self.stacked_collection_page.widget(i)

            if i < new_page_count:
                item_per_page = item_list[i * self.number_of_items_on_page: (i + 1) * self.number_of_items_on_page]
                single_page.set_item_list(item_per_page)

            else:
                self.stacked_collection_page.removeWidget(single_page)
                single_page.deleteLater()

        for i in range(self.stacked_collection_page.count(), new_page_count):

            single_collection_page = CollectionSinglePage(
                item_service=self.item_service,
                stacked_widget=self.stacked_widget,
                page_idx=i,
                item_list= item_list[i * self.number_of_items_on_page: (i + 1) * self.number_of_items_on_page]
            )
            single_collection_page.setParent(self)
            self.stacked_collection_page.addWidget(single_collection_page)

        self.page_count = new_page_count
        self.current_page_idx = min(self.current_page_idx, self.page_count - 1)
        self.stacked_collection_page.setCurrentIndex(self.current_page_idx)
        self.update()

    def init_tool_bar(self):

        tool_bar_layout = QHBoxLayout()

        self.input_search.setPlaceholderText("What are you looking for?")
        self.input_search.setFixedHeight(30)

        search_button = QPushButton("Search")
        search_button.setFixedHeight(30)
        search_button.clicked.connect(lambda: self.search(self.input_search.text().strip()))

        sort_label = QLabel("Sort by:")
        sort_label.setMaximumHeight(30)
        order_label = QLabel("Order:")
        order_label.setMaximumHeight(30)

        self.sort_dropdown.addItems(
            [
                "Default",
                "Name",
                "Finding date",
                "Addition date",
                "Quantity",
                "Finder name",
                "Locality name",
                "Location name",
                "Material name",
                "Year",
            ]
        )
        self.sort_dropdown.setFixedHeight(30)
        self.sorting_order.addItem("Ascending", False)
        self.sorting_order.addItem("Descending", True)

        self.sorting_order.setMaximumHeight(30)

        tool_bar_layout.addWidget(self.input_search)
        tool_bar_layout.addWidget(sort_label)
        tool_bar_layout.addWidget(self.sort_dropdown)
        tool_bar_layout.addWidget(order_label)
        tool_bar_layout.addWidget(self.sorting_order)
        tool_bar_layout.addWidget(search_button)

        self.layout.addLayout(tool_bar_layout, 1, 1, 1, 3)

    def init_filter_bar(self) -> None:
        while self.filter_bar_layout.count():
            item = self.filter_bar_layout.takeAt(0)
            if widget := item.widget():
                self.filter_bar_layout.removeWidget(widget)
                widget.deleteLater()
            else:
                self.clear_layout(item)

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

        quantity_label = QLabel("Quantity")
        quantity_label.setMaximumWidth(250)
        quantity_label.setFont(QFont("Cambria Math", 12, QFont.Weight.Bold))

        quantity_validator = QIntValidator()
        quantity_validator.setRange(0, 1000)
        quantity_min_range = QLineEdit(self)
        quantity_min_range.setValidator(quantity_validator)
        quantity_min_range.setPlaceholderText("from")
        quantity_min_range.setMaximumWidth(150)

        quantity_max_range = QLineEdit(self)
        quantity_max_range.setValidator(quantity_validator)
        quantity_max_range.setPlaceholderText("to")
        quantity_max_range.setMaximumWidth(150)

        finding_date_label = QLabel("Finding date")
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

        year_label = QLabel("Year")
        year_label.setMaximumWidth(250)
        year_label.setFont(QFont("Cambria Math", 12, QFont.Weight.Bold))

        year_validator = QIntValidator()
        year_validator.setRange(0, 1000)
        year_min_range = QLineEdit(self)
        year_min_range.setValidator(year_validator)
        year_min_range.setPlaceholderText("from")
        year_min_range.setMaximumWidth(150)

        year_max_range = QLineEdit(self)
        year_max_range.setValidator(year_validator)
        year_max_range.setPlaceholderText("to")
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
            widget.setPlaceholderText(f"Enter {label}")
            widget_label = QLabel(label)
            widget_label.setMaximumWidth(250)
            widget_label.setFont(QFont("Cambria Math", 12, QFont.Weight.Bold))

            self.filter_bar_layout.addWidget(widget_label)
            self.filter_bar_layout.addWidget(widget)
            self.create_filter_checkbox(label)

        filter_button = QPushButton("Filter")
        filter_button.setStyleSheet(main_button_style)
        filter_button.setMaximumWidth(100)
        filter_button.setMaximumHeight(60)
        filter_button.clicked.connect(self.filter)

        self.filter_bar_layout.addWidget(
            filter_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.layout.addLayout(self.filter_bar_layout, 1, 0, 4, 1)

    def go_to_start_window(self):
        self.stacked_widget.setCurrentIndex(0)

    def search(self, item_name: str) -> None:

        sorting_column_name = self.sort_dropdown.currentText()

        sorting_order = self.sorting_order.currentData()

        if not item_name:
            print(f'{sorting_column_name=}')
            founded_items = self.item_service.founded_items_repository.get_all_items_order_by(
                value=sorting_column_name,
                descending=sorting_order
            )
            print(f'{founded_items=}')
            self.create_single_pages(item_list=founded_items, is_searching=False)

        else:

            founded_items = (
                self.item_service.founded_items_repository.get_all_item_where_value_equals(
                    value="Item name",
                    variable=item_name,
                    column_to_order=item_attributes_to_db_column_mapping[sorting_column_name],
                    descending=sorting_order,
                )
            )
            print(f'tutaj')
            print(f'{founded_items=}')
            self.create_single_pages(item_list=founded_items, is_searching=True)

    def filter(self) -> None:

        equals_criteria, range_criteria = self.get_filters_values()
        item_name = self.input_search.text()
        sorting_column_name = item_attributes_to_db_column_mapping[
            self.sort_dropdown.currentText()
        ]
        sorting_order = self.sorting_order.currentData()

        if item_name:
            equals_criteria[item_attributes_to_db_column_mapping['Name']] = f"('{item_name}')"

        founded_items = self.item_service.founded_items_repository.fetch_items_with_criteria(
            equals_criteria=equals_criteria,
            range_criteria=range_criteria,
            order_column=sorting_column_name,
            descending=sorting_order
        )
        self.create_single_pages(item_list=founded_items, is_searching=True)

    def go_to_next_page(self):
        if self.current_page_idx < self.page_count - 1:
            self.current_page_idx += 1
            self.stacked_collection_page.setCurrentIndex(self.current_page_idx)

    def go_to_previous_page(self):
        if self.current_page_idx > 0:
            self.current_page_idx -= 1
            self.stacked_collection_page.setCurrentIndex(self.current_page_idx)

    def filter_options(self, category_name: str):

        match category_name:
            case "Finder name":
                return [
                    QCheckBox(finder_name)
                    for finder_name in self.item_service.finder_repository.get_all_finder_name()[
                        :4
                    ]
                ]

            case "Locality name":
                return [
                    QCheckBox(locality_name)
                    for locality_name in self.item_service.locality_repository.get_all_locality_name()[
                        :4
                    ]
                ]

            case "Location name":
                return [
                    QCheckBox(location_name)
                    for location_name in self.item_service.location_repository.get_all_location_name()[
                        :4
                    ]
                ]

            case "Material name":
                return [
                    QCheckBox(material_name)
                    for material_name in self.item_service.material_repository.get_all_material_name()[
                        :4
                    ]
                ]

            case "Epoch name":
                return [
                    QCheckBox(epoch_name)
                    for epoch_name in self.item_service.dating_repository.get_all_epoch_name()[
                        :4
                    ]
                ]

    def create_filter_checkbox(self, filter_name: str) -> None:
        if options := self.filter_options(filter_name):
            for i in range(0, len(options), 2):
                op_layout = QHBoxLayout(self)
                op_layout.setSpacing(10)
                op_layout.addWidget(options[i])
                if i + 1 < len(options):
                    op_layout.addWidget(options[i + 1])
                self.filter_bar_layout.addLayout(op_layout)

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

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

            if isinstance(widget, QLabel) and widget.text() in [
                "Quantity",
                "Finding date",
                "Year",
            ]:
                r_min = (
                    self.filter_bar_layout.itemAt(i + 1).widget()
                    if i + 1 < self.filter_bar_layout.count()
                    else None
                )
                r_max = (
                    self.filter_bar_layout.itemAt(i + 2).widget()
                    if i + 2 < self.filter_bar_layout.count()
                    else None
                )

                if r_min and r_max:

                    if isinstance(r_min, QLineEdit):
                        r_min.textChanged.connect(
                            lambda _, w=r_min: self.reset_style(w)
                        )
                        r_max.textChanged.connect(
                            lambda _, w=r_max: self.reset_style(w)
                        )

                        min_val = r_min.text()
                        max_val = r_max.text()

                        if max_val and not min_val:
                            mark_invalid(
                                r_min, f"Low {widget.text()} range limit is required"
                            )
                        elif min_val and not max_val:
                            mark_invalid(
                                r_max, f"Upper {widget.text()} range limit is required"
                            )
                        elif min_val and max_val:
                            try:
                                if int(min_val) > int(max_val):
                                    r_min.setText("")
                                    r_max.setText("")
                                    mark_invalid(r_min, f"Range is incorrect")
                                    mark_invalid(r_max, f"Range is incorrect")
                            except ValueError:
                                mark_invalid(r_min, f"Invalid number")
                                mark_invalid(r_max, f"Invalid number")

                    elif isinstance(r_min, QDateEdit):

                        min_date = r_min.date().toString("yyyy-MM-dd")
                        max_date = r_max.date().toString("yyyy-MM-dd")

                        if min_date > max_date:
                            QMessageBox.warning(
                                self,
                                "Incorrect finding date range",
                                "Lower date should be earlier than upper one",
                            )

                            errors.append("Incorrect year range")

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
                    if name in ["Quantity", "Year"]:
                        min_widget = widget
                        max_widget = self.filter_bar_layout.itemAt(i + 1).widget()

                        if max_widget and isinstance(max_widget, QLineEdit):
                            min_value = min_widget.text()
                            max_value = max_widget.text()
                            if name:
                                range_filters[
                                    item_attributes_to_db_column_mapping[name]
                                ] = (min_value, max_value)
                            i += 1
                    else:
                        if name and widget.text():
                            single_value_filters[
                                item_attributes_to_db_column_mapping[name]
                            ] = [widget.text()]

                elif widget and isinstance(widget, QDateEdit):
                    min_widget = widget
                    max_widget = self.filter_bar_layout.itemAt(i + 1).widget()

                    if max_widget and isinstance(max_widget, QDateEdit):
                        min_date = min_widget.date().toString("yyyy-MM-dd")
                        max_date = max_widget.date().toString("yyyy-MM-dd")
                        if name:
                            range_filters[
                                item_attributes_to_db_column_mapping[name]
                            ] = (min_date, max_date)
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
                single_value_filters[key] = (
                    tuple(values) if len(values) > 1 else f"('{values[0]}')"
                )

            return single_value_filters, range_filters
