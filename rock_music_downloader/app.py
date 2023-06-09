import os
import re
from typing import Callable

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from database import MusicDbManager
from data_collection import Parser
import app_images_rc


class Ui_MainWindow(QMainWindow):
    """

    Main class of the application.
    """
    def __init__(self):
        super().__init__()

        self.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.setStyleSheet("border-image: url(images/metall.jpg);")

        self.db_instance = MusicDbManager()
        self.parser = Parser()

        self.vbox = QtWidgets.QVBoxLayout(self.centralwidget)

        self.show_all_bands_button = self.push_button_create(
                'show_all_bands_button', 'Show all bands',
                70, self.show_all_bands_button_slot
                )

        self.show_genres_button = self.push_button_create(
                'show_genres_button', 'Show genres',
                70, self.show_genres_button_slot
                )

        self.start_notice = self.log_label_create('start_notice', 30)
        self.start_notice.hide()
        self.log_from_parser_module = self.log_label_create(
                'log_from_parser_module', 15
                )
        self.log_from_parser_module.hide()
        self.albums_pbar = self.create_progress_bar('albums_pbar')
        self.albums_pbar.hide()

        self.log_from_writer_module = self.log_label_create(
                'log_from_writer_module', 15
                )
        self.log_from_writer_module.hide()
        self.songs_pbar = self.create_progress_bar('songs_pbar')
        self.songs_pbar.hide()

        self.music_list = self.list_widget_create(
                'music_list', self.parser_lounch
                )
        self.music_list.addItems(self.db_instance.show_all_bandnames_or_genges('band_name'))
        self.search_bar = self.search_bar_create()
        self.music_list.hide()

        self.genres_list = self.list_widget_create(
                'genres_list', self.show_music_of_the_selected_genre
                )
        self.genres_list.addItems(self.db_instance.show_all_bandnames_or_genges('genre'))
        self.genres_list.hide()

        self.search_music_list = self.list_widget_create(
                'search_music_list', self.parser_lounch
                )
        self.search_music_list.hide()

        self.back_button = self.push_button_create(
                'back_button', '<<Back', 13, self.back_button_slot
                )
        self.back_button.hide()
        self.back_to_genre_button = self.push_button_create(
                'back_to_genre_button', '<<Back to genres',
                13, self.back_to_genre_button_slot
                )
        self.back_to_genre_button.hide()

    def parser_lounch(self, item) -> None:
        self.back_button.hide()
        self.back_to_genre_button.hide()
        self.list.hide()

        self.parser.path_for_music = self.file_dialog().strip()

        selected_band = self.db_instance.band_selection(item.text())
        self.parser.link_to_selected_band = selected_band

        filtered_band_name = self.parser.band_name = re.sub(r'[><:"/\|?*]', '_', item.text()).strip()

        full_path = os.path.normpath(os.path.join(self.parser.path_for_music, filtered_band_name))
        if not os.path.exists(full_path):
            os.mkdir(full_path)

        self.live_albums = self.msg_box_create(
                'Do you need live albums?', (QMessageBox.Yes, QMessageBox.No),
                self.user_answer
                )

        self.music_list.hide()
        self.search_bar.hide()
        self.search_music_list.hide()

        self.log_from_writer_module.show()
        self.log_from_parser_module.show()
        self.start_notice.setText(f'{filtered_band_name}\nis downloading...')
        self.start_notice.show()

        self.albums_pbar.show()
        self.songs_pbar.show()

        self.parser.parse(self.log_from_parser_module, self.log_from_writer_module, self.albums_pbar, self.songs_pbar)

        self.log_from_writer_module.hide()
        self.log_from_parser_module.hide()
        self.start_notice.hide()

        self.show_all_bands_button.show()
        self.show_genres_button.show()
        self.search_bar.clear()
        self.search_bar.show()

        self.albums_pbar.hide()
        self.songs_pbar.hide()

        self.completion_notice = self.msg_box_create(
                f'Downloading is complete.\nMusic is here:\n{full_path}', (QMessageBox.Ok,)
                )

    def show_music_of_the_selected_genre(self, item) -> None:
        """

        This method is genres_list's slot.
        """
        self.music_by_genre_list = self.list_widget_create(
                'music_by_genre_list',
                self.parser_lounch
                )
        self.music_by_genre_list.addItems(self.db_instance.get_bands_of_selected_genre(item.text()))

        self.back_button.hide()
        self.vbox.addWidget(self.music_by_genre_list)
        self.music_by_genre_list.show()
        self.genres_list.hide()
        self.back_to_genre_button.show()

    def file_dialog(self) -> str:
        """

        This method returns path, that the user's selected in the file dialog.
        """
        path_for_music_recording = QtWidgets.QFileDialog.getExistingDirectory()
        return path_for_music_recording

    def back_button_slot(self) -> None:
        self.music_list.hide()
        self.genres_list.hide()
        self.back_button.hide()
        self.search_bar.hide()
        self.search_bar.clear()
        self.search_music_list.hide()
        self.search_music_list.clear()
        self.show_all_bands_button.show()
        self.show_genres_button.show()
        self.search_bar.show()

    def show_all_bands_button_slot(self) -> None:
        self.music_list.show()
        self.show_all_bands_button.hide()
        self.show_genres_button.hide()
        self.search_bar.hide()
        self.music_list.show()
        self.back_button
        self.back_button.show()
       
    def show_genres_button_slot(self) -> None:
        self.genres_list.show()
        self.show_genres_button.hide()
        self.search_bar.hide()
        self.show_all_bands_button.hide()
        self.genres_list.show()
        self.back_button
        self.back_button.show()

    def back_to_genre_button_slot(self) -> None:
        self.back_to_genre_button.hide()
        self.music_by_genre_list.hide()
        self.back_button.show()
        self.genres_list.show()

    def user_answer(self, button) -> None:
        """

        This method is live_albums's slot.
        """
        self.parser.user_answer = button.text()

    def list_widget_create(
            self, objname: str, slot: Callable[[str], None]) -> QtWidgets.QListWidget:
        list_font = QtGui.QFont()
        list_font.setPointSize(15)

        self.list = QtWidgets.QListWidget(self)
        self.list.setObjectName(objname)
        self.list.setFont(list_font)
        self.list.setStyleSheet("color: rgb(39, 39, 39);")
        self.list.itemClicked.connect(slot)

        self.vbox.addWidget(self.list)
        return self.list

    def msg_box_create(self, message: str, buttons: tuple, slot: Callable[[str], None] | None=None) -> None:
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Notification')
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        if len(buttons) > 1:
            for button in buttons:
                msg_box.addButton(button)
        else:
            msg_box.addButton(buttons[0])

        if slot:
            msg_box.buttonClicked.connect(slot)

        msg_box.exec_()

    def log_label_create(self, obj_name: str, font_size: int) -> QtWidgets.QLabel:
        font = QtGui.QFont()
        font.setPointSize(font_size)
        
        self.log = QtWidgets.QLabel(self)
        self.log.setObjectName(obj_name)
        self.log.setFont(font)
        self.log.setStyleSheet("color: rgb(39, 39, 39);")

        self.vbox.addWidget(self.log)
        return self.log

    def push_button_create(self, obj_name: str, text: str,
                           font_size: int, slot: Callable[[], None]
                           ) -> QtWidgets.QPushButton:
        self.pushButton = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(font_size)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(70)
        font.setStrikeOut(False)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("color: rgb(39, 39, 39);")
        self.pushButton.setObjectName(obj_name)
        self.pushButton.setText(text)
        self.pushButton.clicked.connect(slot)

        self.vbox.addWidget(self.pushButton)
        return self.pushButton

    def create_progress_bar(self, obj_name: str, step: int = 0):
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setProperty("value", step)
        self.progressBar.setObjectName(obj_name)
        self.vbox.addWidget(self.progressBar)
        return self.progressBar

    def search_bar_create(self):
        search_bar_font = QtGui.QFont()
        search_bar_font.setPointSize(10)

        self.search_bar = QtWidgets.QLineEdit(self)
        self.search_bar.setFont(search_bar_font)
        self.search_bar.setStyleSheet("color: rgb(39, 39, 39);")
        self.search_bar.setPlaceholderText('Search')
        self.completer = QtWidgets.QCompleter(self.db_instance.show_all_bandnames_or_genges('band_name'))
        self.search_bar.setCompleter(self.completer)
        self.search_bar.textChanged.connect(self.search_bar_slot)
        self.vbox.addWidget(self.search_bar)
        return self.search_bar

    def search_bar_slot(self, text):
        found_music = re.findall(text, str(self.db_instance.show_all_bandnames_or_genges('band_name')))
        if text in self.db_instance.show_all_bandnames_or_genges('band_name'):
            self.search_music_list.clear()
            self.show_all_bands_button.hide()
            self.show_genres_button.hide()
            self.search_music_list.addItems(found_music)
            self.search_music_list.show()
            self.back_button.show()
        else:
            self.show_all_bands_button.show()
            self.show_genres_button.show()
            self.search_music_list.hide()
            self.back_button.hide()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    main_window = Ui_MainWindow()

    main_window.show()

    sys.exit(app.exec_())
