import re

import requests as requests
from bs4 import BeautifulSoup as Bs, PageElement
from datetime import datetime, timedelta

from model import Song
from plugin import plugin
from source.source import Source

def to_timedelta(text):
    date_time = datetime.strptime(text, '%M:%S')
    return timedelta(minutes=date_time.minute, seconds=date_time.second)

def _to_song(node: PageElement):
    title = node.find_next(class_="d-track__title").text.strip()
    artists_node = node.find_next(class_="d-track__artists")
    artists = [n["title"] for n in artists_node.contents if n.name == "a"]
    info_node = node.find_next(class_="d-track__info")
    time = to_timedelta(info_node.span.text.strip()) 

    return Song(title, artists, time, None)


_location_matcher = re.compile(r'^https://music\.yandex\..+/playlists/[0-9]+$')


@plugin
class YandexMusic(Source):

    def get_songs(self, location) -> list[Song]:
        html = requests.get(location).text
        dom = Bs(html, "lxml")
        track_nodes = dom.find_all("div", "d-track")
        return [_to_song(node) for node in track_nodes]

    def match(self, location: str) -> bool:
        return _location_matcher.match(location) is not None
