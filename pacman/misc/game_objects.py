from typing import Iterable, List

from pygame import Surface
from pygame.event import Event

from pacman.data_core import IDrawable, IEventful, ILogical


class GameObjects(List):
    __included_types = (IDrawable, IEventful, ILogical)

    # region Public

    def append(self, item) -> None:
        self.__check_type(item)
        super().append(item)

    def insert(self, index, item) -> None:
        self.__check_type(item)
        super().insert(index, item)

    def extend(self, iterable: Iterable) -> None:
        for item in iterable:
            self.__check_type(item)
        super().extend(iterable)

    def update(self) -> None:
        filtered: Iterable[ILogical] = filter(lambda x: isinstance(x, ILogical), self)
        for obj in filtered:
            obj.update()

    def draw(self, screen: Surface) -> None:
        filtered: Iterable[IDrawable] = filter(lambda x: isinstance(x, IDrawable), self)
        for obj in filtered:
            obj.draw(screen)

    def event_handler(self, event: Event) -> None:
        filtered: Iterable[IEventful] = filter(lambda x: isinstance(x, IEventful), self)
        for obj in filtered:
            obj.event_handler(event)

    # endregion

    # region Private

    def __check_type(self, item):
        if not isinstance(item, self.__included_types):
            raise ValueError(f"Object type: {type(item)}/{item} is not in {self.__included_types}")

    def __iadd__(self, other):
        for item in other:
            self.__check_type(item)
        return super().__iadd__(other)

    # endregion
