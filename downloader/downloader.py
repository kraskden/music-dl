import requests

from model import Song


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

class Downloader:

    def __init__(self, *args, **kwargs):
        self.params = kwargs

    def search(self, query: str) -> list[Song]:
        raise NotImplementedError()

    def search_song(self, song: Song) -> list[Song]:
        raise NotImplementedError()

    def download(self, song: Song) -> bytes:
        raise NotImplementedError()