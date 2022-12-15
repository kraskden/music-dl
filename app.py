import sys
from typing import Optional

from downloader.downloader import SongNotFoundError, QueryNotFoundError
from lib import Lib
from model import Song, DownloadableSong
from picker import select_songs, pick_download_candidate
from plugin import load_dl, load_source


class App:

    def __init__(self, target_path: str, downloader_name: str):
        self.lib = Lib(target_path)
        self.downloader = load_dl(downloader_name)

    def source_download(self, source_url: str, download_all: bool):
        source = load_source(source_url)

        songs = source.get_songs(source_url)
        songs = songs if download_all else select_songs(songs)
        for song in songs:
            try:
                candidates = self.downloader.search_song(song)
                self._download_candidates(candidates, song)
            except SongNotFoundError as e:
                print(f"[ERR] Song {song} not found", file=sys.stderr)

    def interactive_download(self):
        while True:
            try:
                query = input('> ')
                candidates = self.downloader.search(query)
                self._download_candidates(candidates, reference=None)
            except QueryNotFoundError as e:
                print(f'[ERR] Nothing found by query {e.query}')
            except (EOFError, KeyboardInterrupt):
                break

    def _download_candidates(self, candidates: list[DownloadableSong], reference: Optional[Song]) -> bool:
        target = pick_download_candidate(reference, candidates)
        if target is None:
            print(f"[WARN] Skip downloading")
            return False
        data = target.download()
        self.lib.saveMP3(data, target)

        print(f'[OK] {target}')
        return True
