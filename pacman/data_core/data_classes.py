from dataclasses import dataclass


@dataclass
class Cell:
    __x: int
    __y: int

    @property
    def x(self) -> int:
        return self.__x * 8

    @property
    def y(self) -> int:
        return self.__y * 8 + 20


@dataclass
class ResolutionSize:
    WIDTH: int
    HEIGHT: int

    @property
    def half_width(self) -> int:
        return self.WIDTH // 2

    @property
    def half_height(self) -> int:
        return self.HEIGHT // 2

    def __iter__(self):
        yield self.WIDTH
        yield self.HEIGHT
