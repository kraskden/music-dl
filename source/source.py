from model import Song


class Source:

    def __init__(self, *args, **kwargs):
        self.params = kwargs

    def match(self, location: str) -> bool:
        return False

    def get_songs(self, location) -> list[Song]:
        pass
