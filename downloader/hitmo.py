import requests
from bs4 import BeautifulSoup as Bs, PageElement

from downloader.downloader import Downloader, SongNotFoundError, download, QueryNotFoundError, UrlDownloadableSong
from model import Song, DownloadableSong
from plugin import plugin
from util import to_timedelta

"""
Download music from https://in.hitmo.top
"""


def _to_song(node: PageElement) -> DownloadableSong:
    title = node["data-title"]
    artist = node["data-artist"]
    try:
        time = to_timedelta(node["data-duration"].strip())
    except ValueError:
        time = None
    url = node.find_next("div", "play")["data-url"]

    return UrlDownloadableSong(title, [artist], time, None, url)


@plugin
class HitmoDownloader(Downloader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = kwargs["url"] if "url" in kwargs else "https://in.hitmo.top/search"

    def search(self, query: str) -> list[DownloadableSong]:
        html = requests.get(self.url, params={"q": query}).text
        dom = Bs(html, "lxml")

        tracks_nodes = dom.find_all("li", "item")
        if len(tracks_nodes) == 0:
            raise QueryNotFoundError(query)
        return [_to_song(node) for node in tracks_nodes]

    def search_song(self, song: Song) -> list[DownloadableSong]:
        query = f'{song.title} + {" ".join(song.author)}'
        try:
            return self.search(query)
        except QueryNotFoundError:
            raise SongNotFoundError(song)