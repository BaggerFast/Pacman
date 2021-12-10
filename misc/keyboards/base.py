import dataclasses
import pygame as pg

from misc import event_append


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
                event_append(key.event)
                return

    def process_logic(self):
        keys = pg.key.get_pressed()
        for kb in self.data_keys:
            for key in kb.keys:
                if keys[key]:
                    event_append(kb.event)
                    return
