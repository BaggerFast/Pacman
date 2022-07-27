import pygame as pg
from pacman.misc.interfaces import ILogical, IEventful, IDrawable, IGenericObject


class Objects(IGenericObject):
    _allowed_types = (ILogical, IEventful, IDrawable)

    def __init__(self, *args):
        self.__obj = self.__parse_list(args)

    # region Private

    def __parse_list(self, data: tuple) -> list:
        return list(map(self.__check_types, data))

    def __check_types(self, obj):
        if isinstance(obj, self._allowed_types):
            return obj
        raise TypeError(f"class Object поддерживает добавление только {self._allowed_types}")

    # endregion

    # region Public

    # region Implementation of IGenericObject

    def process_draw(self, screen: pg.Surface) -> None:
        filtered = filter(lambda x: isinstance(x, IDrawable), self.__obj)
        for obj in filtered:
            obj.process_draw(screen)
            obj.additional_draw(screen)

    def process_event(self, event: pg.event.Event) -> None:
        filtered = filter(lambda x: isinstance(x, IEventful), self.__obj)
        for obj in filtered:
            obj.process_event(event)
            obj.additional_event(event)

    def process_logic(self) -> None:
        filtered = filter(lambda x: isinstance(x, ILogical), self.__obj)
        for obj in filtered:
            obj.process_logic()
            obj.additional_logic()

    # endregion

    def append(self, *args) -> None:
        self.__obj.extend(self.__parse_list(args))

    def clear(self) -> None:
        self.__obj.clear()

    def __getitem__(self, index: int):
        return self.__obj[index]

    def __len__(self) -> int:
        return len(self.__obj)

    # endregion
