import os
import re

from PyQt5 import QtWidgets

from tools import session


class Saver:
    def __init__(self):
        self.album_refs = str()
        self.album_name = str()
        self.band_name = str()

        self.path_for_music = str()

    def download_songs(self, log_from_writer_module: QtWidgets.QLabel,
                       step_for_songpb):
        """
        Download and save all albums with .mp3 songs.
        """
        response = session.get(url=self.album_refs).text
        filtered_band_name = self.record_path_filter(self.band_name)
        filtered_album_name = self.record_path_filter(self.album_name)
        os.mkdir(
            os.path.normpath(
                os.path.join(self.path_for_music, filtered_band_name, filtered_album_name)
                )
            )
        # regex, parse links from JS.
        pattern_of_ref = re.findall(
            r'http://rocknation\.su/upload/mp3/.+?\.mp3',
            response
        )
        song_count = 1
        step = 100 / len(pattern_of_ref)
        # download songs.
        for i in pattern_of_ref:
            download = session.get(url=i).content
            # Get the name of the song from song link.
            pattern_of_name = re.findall(r'\d\.(.+)\.mp3', i)[0]
            # Cleaning the name of the song.
            song_name = re.sub(r'[\d %]', r'', pattern_of_name)

            self.music_recording(download, song_count, pattern_of_ref,
                                 song_name, log_from_writer_module,
                                 filtered_band_name, filtered_album_name)
            step_for_songpb.setProperty("value", step)
            step += 100 / len(pattern_of_ref)
            song_count += 1

    @staticmethod
    def record_path_filter(piese_of_path: str) -> str:
        filtered_piese_of_path = re.sub(r'[><:"/\|?*]', '_', piese_of_path).strip()
        return filtered_piese_of_path

    def music_recording(self, download, song_count: int, pattern_of_ref: list,
                        song_name: str, log_from_writer_module: QtWidgets.QLabel,
                        filtered_band_name: str, filtered_album_name: str) -> None:
            music_path = os.path.normpath(
                os.path.join(self.path_for_music, filtered_band_name, filtered_album_name, f'{song_count}. {song_name}.mp3')
            )
            with open(music_path, 'wb') as file:
                file.write(download)

            log_from_writer_module.setText(f'Song: {song_name} {song_count} / {len(pattern_of_ref)}')

            QtWidgets.QApplication.processEvents()

