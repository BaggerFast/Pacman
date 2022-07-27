from abc import abstractmethod, ABC
import pygame as pg


class IDrawable(ABC):
    """Interface for objects with draw functional"""

    @abstractmethod
    def process_draw(self, screen: pg.Surface) -> None:
        pass

    def additional_draw(self, screen: pg.Surface) -> None:
        pass


class ILogical(ABC):
    """Interface for objects with logical functional"""

    @abstractmethod
    def process_logic(self) -> None:
        pass

    def additional_logic(self) -> None:
        pass


class IEventful(ABC):
    """Interface for objects with event functional"""

    @abstractmethod
    def process_event(self, event: pg.event.Event) -> None:
        pass

    def additional_event(self, event: pg.event.Event) -> None:
        pass


class IGenericObject(IDrawable, ILogical, IEventful, ABC):
    """Interface for objects with draw, event and logical functional"""

    @abstractmethod
    def process_event(self, event: pg.event.Event) -> None:
        pass

    @abstractmethod
    def process_logic(self) -> None:
        pass

    @abstractmethod
    def process_draw(self, screen: pg.Surface) -> None:
        pass
