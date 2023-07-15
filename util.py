from datetime import timedelta, datetime


def to_timedelta(text: str) -> timedelta:
    seconds = int(text)
    return timedelta(minutes=(seconds // 60), seconds=(seconds % 60))
