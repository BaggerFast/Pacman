from dataclasses import dataclass
from typing import Callable

from pygame import Rect


@dataclass(frozen=True)
class GhostDifficult:
    frightened: int
    chase: int
    scatter: int


@dataclass(frozen=True)
class Direction:
    x: int
    y: int
    rotate: int


@dataclass(frozen=True)
class Cheat:
    cheat_code: str
    function: Callable

    def __call__(self):
        self.function()


@dataclass(frozen=True)
class Cell:
    x: int
    y: int

    @property
    def rect(self):
        return Rect(self.x * 8, self.y * 8 + 20, 8, 8)


@dataclass(frozen=True)
class ResolutionSize:
    WIDTH: int
    HEIGHT: int

    @property
    def h_width(self) -> int:
        return self.WIDTH // 2

    @property
    def h_height(self) -> int:
        return self.HEIGHT // 2

    def __iter__(self):
        yield self.WIDTH
        yield self.HEIGHT
