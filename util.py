from datetime import timedelta, datetime


def to_timedelta(text: str) -> timedelta:
    t = datetime.strptime(text, "%M:%S")
    return timedelta(minutes=t.minute, seconds=t.second)
