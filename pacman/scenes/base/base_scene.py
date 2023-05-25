from abc import ABC
from typing import Generator

from pygame import Surface, time
from pygame.event import Event

from pacman.data_core import Cfg, Colors
from pacman.misc import GameObjects


class BaseScene(ABC):
    def __init__(self):
        self._start_time = time.get_ticks() / 1000
        self._screen = Surface(tuple(Cfg.RESOLUTION))
        self._objects = GameObjects()

    # region Private

    def _generate_objects(self) -> Generator:
        raise NotImplementedError

    # endregion

    # region Public

    def draw(self) -> Surface:
        self._screen.fill(Colors.BLACK)
        self._objects.draw(self._screen)
        return self._screen

    def process_logic(self) -> None:
        self._objects.update()

    def process_event(self, event: Event) -> None:
        self._objects.event_handler(event)

    def setup(self):
        self._objects.clear()
        if obj := self._generate_objects():
            self._objects.extend(list(obj))

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    def on_first_enter(self) -> None:
        pass

    def on_last_exit(self) -> None:
        pass

    # endregion
