from dataclasses import dataclass


@dataclass
class Cell:
    x: int
    y: int


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
