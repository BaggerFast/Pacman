from copy import copy

from pygame import Surface

from pacman.animator import sprite_slice
from pacman.data_core import Cfg, Colors, IDrawable
from pacman.misc import ImgObj


class Map(IDrawable):
    def __init__(self, map_data: list[list[int]], color=Colors.MAIN_MAP) -> None:
        self._color = color
        self._map_data = map_data
        self._tiles = sprite_slice("other/map", (8, 8))
        self._image = self.__load_surface()
        self.surface_for_draw = self.__surface_recolor()

    def __surface_recolor(self) -> Surface:
        if self._color == Colors.MAIN_MAP:
            return copy(self._image)
        srf = copy(self._image)
        for x in range(srf.get_width()):
            for y in range(srf.get_height()):
                if srf.get_at((x, y)) == Colors.MAIN_MAP:
                    srf.set_at((x, y), self._color)
        return srf

    def __load_surface(self) -> Surface:
        surface = Surface((len(self._map_data[0]) * Cfg.TILE_SIZE, len(self._map_data) * Cfg.TILE_SIZE))
        for y, row in enumerate(self._map_data):
            for x, tile in enumerate(row):
                surface.blit(self._tiles[tile - 1], (x * Cfg.TILE_SIZE, y * Cfg.TILE_SIZE))
        return surface

    def prerender(self) -> ImgObj:
        return ImgObj(copy(self._image))

    def draw(self, screen: Surface) -> None:
        screen.blit(self.surface_for_draw, (0, 20))
