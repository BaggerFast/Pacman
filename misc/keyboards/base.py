import dataclasses
import pygame as pg


class BaseKeyboard:
    @dataclasses.dataclass
    class KeyControl:
        keys: list
        event: int

    data_keys = []

    def __init__(self):
        self.configure()

    def configure(self) -> None:
        raise NotImplementedError

    def process_event(self, event: pg.event) -> None:
        if event.type != pg.KEYDOWN:
            return
        for key in self.data_keys:
            if event.key in key.keys:
                pg.event.post(pg.event.Event(key.event))
                return
