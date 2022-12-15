import os.path
import re

from model import Song
from mutagen.id3 import ID3, TIT2, TPE1

class Lib:

    def __init__(self, dir_path):
        if not os.path.isdir(dir_path):
            raise ValueError(f"{dir_path} must be a directory")
        self.dir_path = dir_path

    def saveMP3(self, data: bytes, meta: Song):
        path = os.path.join(self.dir_path, _get_path(meta))
        with open(path, 'w+b') as f:
            f.write(data)
        audion = ID3(path)
        audion.clear()
        audion.add(TIT2(text=meta.title))
        audion.add(TPE1(text=meta.author))
        audion.save()


def _get_path(song: Song) -> str:
    author = song.author[0] if len(song.author) > 0 else None
    name = f'{author}__{song.title}.mp3' if author is not None else f'{song.title}'
    return _replace_whitespaces(name)

_ws_regex = re.compile(r'\s')
def _replace_whitespaces(text: str):
    return _ws_regex.sub('-', text)