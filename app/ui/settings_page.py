from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QCheckBox,
    QSlider,
    QSizePolicy,
)
from PyQt6.QtMultimedia import QSoundEffect


class SettingPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.stacked_page = stacked_widget
        self.music_checkboxes = []
        self.music_files = [
            "Around the World",
            "Gummy bear",
            "Katioucha",
            "Lay All Your Love On Me",
            "Revolutionary Etude",
            "Rondo Alla Turca",
        ]
        self.sound = QSoundEffect()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        settings_label = QLabel("Settings")
        settings_label.setFont(QFont("Cambria Math", 30, QFont.Weight.DemiBold))
        layout.addWidget(settings_label, alignment=Qt.AlignmentFlag.AlignCenter)


        music_label = QLabel("Select background music")
        music_label.setFont(QFont("Cambria Math", 15, QFont.Weight.DemiBold))
        layout.addWidget(music_label, alignment=Qt.AlignmentFlag.AlignCenter)


        for title in self.music_files:
            checkbox = QCheckBox(title)
            checkbox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            checkbox.setMinimumWidth(155)
            checkbox.stateChanged.connect(self.on_checkbox_clicked)
            self.music_checkboxes.append(checkbox)
            layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignCenter)

        volume_label = QLabel("Volume")
        volume_label.setFont(QFont("Cambria Math", 15, QFont.Weight.DemiBold))
        layout.addWidget(volume_label)

        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setMaximumWidth(200)
        self.volume_slider.valueChanged.connect(self.set_volume)
        layout.addWidget(self.volume_slider)


        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.toggle_playback)
        layout.addWidget(self.play_button, alignment=Qt.AlignmentFlag.AlignCenter)


        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back_to_start_page)
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_checkbox_clicked(self, state):
        sender = self.sender()
        if state:
            for checkbox in self.music_checkboxes:
                if checkbox is not sender:
                    checkbox.setChecked(False)

    def play_selected_music(self):
        selected_music = next(
            (cb.text() for cb in self.music_checkboxes if cb.isChecked()), None
        )
        if selected_music:
            music_path = "ui/background_music/" + selected_music + ".wav"
            self.sound = QSoundEffect()
            self.sound.setLoopCount(1000)
            self.sound.setSource(QUrl.fromLocalFile(music_path))
            self.sound.play()
            self.play_button.setText("Pause")
        else:
            self.sound.stop()
            self.play_button.setText("Play")

    def toggle_playback(self):
        if self.sound.isPlaying():
            self.sound.stop()
            self.play_button.setText("Play")
        else:
            self.play_selected_music()

    def set_volume(self, value):
        self.sound.setVolume(value / 100)

    def back_to_start_page(self):
        self.stacked_page.setCurrentIndex(0)
