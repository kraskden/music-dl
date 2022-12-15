import requests
from bs4 import BeautifulSoup as Bs, PageElement

from downloader.downloader import Downloader, SongNotFoundError, download, QueryNotFoundError, UrlDownloadableSong
from model import Song, DownloadableSong
from plugin import plugin
from util import to_timedelta

"""
Download music from https://eu.hitmotop.com
"""


def _to_song(node: PageElement) -> DownloadableSong:
    title = node.find_next(class_="track__title").text.strip()
    artist = node.find_next(class_="track__desc").text.strip()
    try:
        time = to_timedelta(node.find_next(class_="track__fulltime").text.strip())
    except ValueError:
        time = None
    url = node.find_next("a", class_="track__download-btn")["href"]

    return UrlDownloadableSong(title, [artist], time, None, url)


@plugin
class HitmoDownloader(Downloader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = kwargs["url"] if "url" in kwargs else "https://eu.hitmotop.com/search"

    def search(self, query: str) -> list[DownloadableSong]:
        html = requests.get(self.url, params={"q": query}).text
        dom = Bs(html, "lxml")
        tracks_nodes = dom.find_all("div", "track__info")
        if len(tracks_nodes) == 0:
            raise QueryNotFoundError(query)

        return [_to_song(node) for node in tracks_nodes]

    def search_song(self, song: Song) -> list[DownloadableSong]:
        query = f'{song.title} + {" ".join(song.author)}'
        try:
            return self.search(query)
        except QueryNotFoundError:
            raise SongNotFoundError(song)
