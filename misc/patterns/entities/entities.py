import pygame as pg
from abc import ABC


class RenderEntity:

    def render(self, screen: pg.Surface) -> None:
        raise NotImplementedError


class EventEntity:

    def event_handler(self, event: pg.event.Event) -> None:
        raise NotImplementedError


class UpdateEntity(ABC):

    def update(self) -> None:
        raise NotImplementedError


class FullEntity(RenderEntity, EventEntity, UpdateEntity, ABC):
    pass
