from misc.patterns.entities import RenderEntity, EventEntity, UpdateEntity
import pygame as pg


class PoolEntity:
    _allowed_types = (RenderEntity, EventEntity, UpdateEntity)

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

    def render(self, screen: pg.Surface) -> None:
        filtered: filter[RenderEntity] = filter(lambda x: isinstance(x, RenderEntity), self.__obj)
        for obj in filtered:
            obj.render(screen)

    def event_handler(self, event: pg.event.Event) -> None:
        filtered: filter[EventEntity] = filter(lambda x: isinstance(x, EventEntity), self.__obj)
        for obj in filtered:
            obj.event_handler(event)

    def update(self) -> None:
        filtered: filter[UpdateEntity] = filter(lambda x: isinstance(x, UpdateEntity), self.__obj)
        for obj in filtered:
            obj.update()

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
