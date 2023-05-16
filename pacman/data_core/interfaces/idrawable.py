from abc import ABC

from pygame import Surface


class IDrawable(ABC):
    def draw(self, screen: Surface) -> None:
        raise NotImplementedError
