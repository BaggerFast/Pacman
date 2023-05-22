from abc import ABC

from pygame.event import Event


class IEventful(ABC):
    def event_handler(self, event: Event) -> None:
        raise NotImplementedError
