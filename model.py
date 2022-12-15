import re
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional


@dataclass
class Song:
    title: str
    author: list[str]
    duration: Optional[timedelta]
    meta: Optional[dict]

    def __str__(self):
        return f'{",".join(self.author)}: {self.title}, [{self.duration}]'

    def normalize(self) -> 'Song':
        return Song(_normalize_name(self.title), [_normalize_name(a) for a in self.author],
                    self.duration, self.meta)

    def precision_equals(self, song: 'Song', precision_seconds: int) -> bool:
        if song is None:
            return False
        common_authors = set(song.author) & set(self.author)
        duration_matches = True

        if song.duration is not None and self.duration is not None:
            a, b = minmax(song.duration, self.duration)
            duration_matches = (b - a).seconds < precision_seconds

        return duration_matches and len(common_authors) > 0 and self.title == song.title


class DownloadableSong(Song):

    def download(self):
        pass

_ch_filter_pattern = re.compile(r'[\W_]')
def _normalize_name(name: Optional[str]) -> Optional[str]:
    if name is None:
        return None
    return _ch_filter_pattern.sub('', name).lower()


def minmax(a, b):
    return min(a, b), max(a, b)
