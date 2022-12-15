from dataclasses import dataclass

import requests

from model import Song, DownloadableSong


def download(url: str) -> bytes:
    return requests.get(url).content

class NotFoundError(Exception):
    pass

class SongNotFoundError(NotFoundError):

    def __init__(self, song: Song):
        self.song = song

class QueryNotFoundError(NotFoundError):

    def __init__(self, query: str):
        self.query = query

@dataclass
class UrlDownloadableSong(DownloadableSong):
    url: str

    def download(self):
        return download(self.url)

class Downloader:

    def __init__(self, *args, **kwargs):
        self.params = kwargs

    def search(self, query: str) -> list[DownloadableSong]:
        raise NotImplementedError()

    def search_song(self, song: Song) -> list[DownloadableSong]:
        raise NotImplementedError()