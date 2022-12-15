import math
import os
import subprocess
import tempfile
from typing import IO, Optional

from model import Song, DownloadableSong


def pick_download_candidate(reference: Optional[Song], candidates: list[DownloadableSong]) -> Optional[DownloadableSong]:
    if reference is not None:
        ref_normalized = reference.normalize()
        for song in candidates:
            if song.normalize().precision_equals(ref_normalized, precision_seconds=5):
                return song
    return _interactive_select(reference, candidates, page_size=10)


def select_songs(songs: list[Song]) -> list[Song]:
    tmp = tempfile.NamedTemporaryFile('w+', delete=False)
    try:
        _write_songs(tmp, songs)
        tmp.close()
        opener = os.getenv("EDITOR") or "xdg-open"
        subprocess.run([opener, tmp.name])
        with open(tmp.name, 'r') as f:
            return _read_filtered_songs(f, songs)
    finally:
        tmp.close()
        os.unlink(tmp.name)


def _read_filtered_songs(f: IO, songs: list[Song]) -> list[Song]:
    result = []
    for line in f:
        line = line.strip()
        if line.startswith('#'):
            continue
        elif len(line) == 0:
            return result
        else:
            try:
                idx = int(line[0:line.index(':')])
                result.append(songs[idx - 1])
            except:
                raise ValueError("Invalid file format")

    return result


def _write_songs(f: IO, songs: list[Song]):
    f.write((
        "# Select songs to download\n"
        "# Lines starting with # is ignored\n"
        "# All lines after empty line are ignored\n"
    ))

    for idx, song in enumerate(songs):
        f.write(f'{idx + 1}: {song}\n')


def _interactive_select(reference: Song, candidates: list[DownloadableSong], page_size: int) -> Optional[DownloadableSong]:
    page = 1
    total_elements = len(candidates)
    total_pages = math.ceil(total_elements * 1.0 / page_size)
    print(f'Searching {reference}')
    print(f'Found {total_elements} candidates')
    while True:
        for i in range((page - 1) * page_size, min(page * page_size, total_elements)):
            print(f'[{i + 1}] {candidates[i]}')
        print(f'Page {page}/{total_pages} [N/P/C]')
        while True:
            try:
                cmd = input('>').capitalize()
            except (EOFError, KeyboardInterrupt):
                return None
            if cmd == 'C':
                return None
            elif cmd == 'N':
                if page < total_pages:
                    page += 1
                    break
                else:
                    print("This is the last page")
            elif cmd == 'P':
                if page > 1:
                    page -= 1
                    break
                else:
                    print("This is the first page")
            else:
                try:
                    num = 1 if cmd == '' else int(cmd)
                    if 0 < num <= page_size:
                        return candidates[num - 1]
                    else:
                        print("Wrong number, try again")
                except ArithmeticError:
                    print("Unknown command")
