from abc import ABC, abstractmethod

import pygame as pg


class IDrawable(ABC):

    @abstractmethod
    def process_draw(self, screen: pg.Surface) -> None: pass

    def additional_draw(self, screen: pg.Surface) -> None: pass


class IEventful(ABC):

    @abstractmethod
    def process_event(self, event: pg.event.Event) -> None: pass

    def additional_event(self, event: pg.event.Event) -> None: pass


class ILogical(ABC):

    @abstractmethod
    def process_logic(self) -> None: pass

    def additional_logic(self) -> None: pass


class IGenericObject(IDrawable, ILogical, IEventful):

    @abstractmethod
    def process_event(self, event: pg.event.Event) -> None: pass

    @abstractmethod
    def process_logic(self) -> None: pass

    @abstractmethod
    def process_draw(self, screen: pg.Surface) -> None: pass
