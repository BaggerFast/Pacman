from typing import NamedTuple, Callable

from pacman.objects import ImageObject, Text


class MenuPreset(NamedTuple):
    name: str
    func: Callable


class Medal(NamedTuple):
    SPRITE: ImageObject
    TEXT: Text

    def process_draw(self, screen):
        self.SPRITE.process_draw()
        self.TEXT.process_draw()
