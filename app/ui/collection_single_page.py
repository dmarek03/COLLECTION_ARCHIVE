from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
)
from app.service.dto import CreateFinalItemDto
from app.utilities.button_style import main_button_style
from app.ui.item_single_page import ItemSinglePage
from app.service.final_item_service import FinalItemService


class CollectionSinglePage(QWidget):
    def __init__(
        self,
        item_service: FinalItemService,
        stacked_widget,
        page_idx: int,
        item_list: list[CreateFinalItemDto],
    ):
        super().__init__()
        self.item_service = item_service
        self.stacked_widget = stacked_widget
        self.page_idx = page_idx
        self.item_list = item_list
        self.single_item_page_list = {}
        self.layout = QVBoxLayout(self)

        self.init_ui()

    def init_ui(self) -> None:
        self.setLayout(self.layout)

        self.show_items()

    def show_items(self) -> None:
        while self.layout.count():
            item = self.layout.takeAt(0)
            if widget := item.widget():
                widget.deleteLater()

        for item in self.item_list:

            item_frame = QFrame()
            item_frame.setFrameShape(QFrame.Shape.Box)
            item_frame.setLineWidth(2)
            item_frame.setMaximumHeight(160)

            item_layout = QHBoxLayout()
            image_label = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(item.first_image_data)
            image_label.setPixmap(
                pixmap.scaled(160, 160, Qt.AspectRatioMode.KeepAspectRatio)
            )
            image_label.setMaximumWidth(160)
            image_label.setMaximumHeight(160)
            item_layout.setSpacing(5)
            item_layout.addWidget(image_label)

            text_layout = QVBoxLayout()
            text_layout.setSpacing(5)

            name_label = QLabel(f"<b>Item name:</b> {item.name}")
            name_label.setFont(QFont("Arial", 12))
            text_layout.addWidget(name_label)

            date_label = QLabel(f"<b>Date of addition:</b> {item.addition_date.date()}")
            date_label.setFont(QFont("Arial", 12))
            text_layout.addWidget(date_label)

            finder_label = QLabel(f"<b>Name of finder:</b> {item.finder_name}")
            finder_label.setFont(QFont("Arial", 12))
            text_layout.addWidget(finder_label)
            text_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            view_detail_button = QPushButton("View detail")
            view_detail_button.setMaximumWidth(100)
            view_detail_button.setMaximumHeight(50)
            view_detail_button.clicked.connect(lambda _, w=item: self.view_detail(w))

            edit_button = QPushButton("Edit")
            edit_button.setMaximumWidth(100)
            edit_button.setMaximumHeight(50)
            edit_button.clicked.connect(lambda _, w=item: self.edit_item(w))

            delete_button = QPushButton("Delete")
            delete_button.setMaximumWidth(100)
            delete_button.setMaximumHeight(50)
            delete_button.clicked.connect(lambda _, w=item: self.delete_item(w))

            vertical_line = QFrame()
            vertical_line.setFrameShape(QFrame.Shape.VLine)
            vertical_line.setFrameShadow(QFrame.Shadow.Sunken)
            vertical_line.setLineWidth(2)
            vertical_line.setMaximumWidth(10)
            item_layout.addWidget(vertical_line, Qt.AlignmentFlag.AlignLeft)
            item_layout.addLayout(text_layout)
            item_layout.addWidget(view_detail_button, Qt.AlignmentFlag.AlignRight)
            item_layout.addWidget(edit_button, Qt.AlignmentFlag.AlignRight)
            item_layout.addWidget(delete_button, Qt.AlignmentFlag.AlignRight)
            item_frame.setLayout(item_layout)

            self.layout.addWidget(item_frame)

        label = QLabel(f"Page {self.page_idx}")
        label_font = QFont("Cambria Math", 10, QFont.Weight.Bold)
        label.setFont(label_font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label)

    def view_detail(self, item) -> None:
        if not self.single_item_page_list.get(item.id):
            new_page = ItemSinglePage(item, self.stacked_widget)
            self.single_item_page_list[item.id] = new_page
            self.stacked_widget.addWidget(new_page)
            self.stacked_widget.setCurrentWidget(new_page)

        else:
            self.stacked_widget.setCurrentWidget(self.single_item_page_list[item.id])

    def edit_item(self, item) -> None:
        print(f'Editing: {item}')
        add_item_page = self.stacked_widget.widget(2)
        self.stacked_widget.setCurrentWidget(add_item_page)
        add_item_page.go_to_edition_page(item)
        if self.single_item_page_list.get(item.id):
            self.single_item_page_list.pop(item.id)

    def delete_item(self, item) -> None:

        button = QMessageBox.question(
            self,
            "Item delete confirmation",
            f"Do you want to delete: <b>{item.name}<b>",
        )

        if button == QMessageBox.StandardButton.Yes:

            for i in reversed(range(self.layout.count())):
                widget = self.layout.itemAt(i).widget()
                self.layout.removeWidget(widget)

            self.item_list.remove(item)
            self.item_service.delete_final_item(item_id=item.id)
            if self.single_item_page_list.get(item.id):
                widget_to_delete = self.single_item_page_list.pop(item.id)
                self.stacked_widget.removeWidget(widget_to_delete)
            collection_page = self.stacked_widget.widget(1)
            collection_page.create_single_pages()
            collection_page.init_filter_bar()

    def set_item_list(self, item_list: list[CreateFinalItemDto]) -> None:
        self.item_list = item_list
        self.show_items()
