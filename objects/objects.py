import pygame as pg
from misc.interfaces import ILogical, IEventful, IDrawable, IGenericObject


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
        for obj in self.__obj:
            if isinstance(obj, IDrawable):
                obj.process_draw(screen)
                obj.additional_draw(screen)

    def process_event(self, event: pg.event.Event) -> None:
        for obj in self.__obj:
            if isinstance(obj, IEventful):
                obj.process_event(event)
                obj.additional_event(event)

    def process_logic(self) -> None:
        for obj in self.__obj:
            if isinstance(obj, ILogical):
                obj.process_logic()
                obj.additional_logic()

    # endregion

    def append(self, *args) -> None:
        self.__obj.extend(self.__parse_list(args))

    def __getitem__(self, index: int):
        return self.__obj[index]

    def __len__(self) -> int:
        return len(self.__obj)

    def clear(self) -> None:
        self.__obj.clear()

    # endregion
