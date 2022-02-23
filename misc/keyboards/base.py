import dataclasses
from abc import ABC

import pygame as pg

from misc import event_append
from misc.interfaces.object_interfaces import IEventful, ILogical


class BaseKeyboard(IEventful, ILogical, ABC):
    @dataclasses.dataclass
    class KeyControl:
        keys: list
        event: int

    keys_control = []

    def process_event(self, event: pg.event) -> None:
        if event.type != pg.KEYDOWN:
            return
        for key in self.keys_control:
            if event.key in key.keys:
                event_append(key.event)
                return

    def process_logic(self):
        pressed_keys = pg.key.get_pressed()
        for kb in self.keys_control:
            for key in kb.keys:
                if pressed_keys[key]:
                    event_append(kb.event)
                    return

