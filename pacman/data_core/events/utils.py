from pygame import event as e

from .events import EvenType


def event_append(event: EvenType) -> None:
    e.post(e.Event(event))
