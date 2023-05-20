from copy import copy

import pygame as pg
from pygame import Surface

from pacman.data_core import Colors, Cfg
from pacman.data_core.interfaces import IDrawable
from pacman.misc.animator.sprite_sheet import sprite_slice
from pacman.objects import ImageObject, MovementObject


class Map(MovementObject, IDrawable):
    def __init__(self, map_data, color=Colors.MAIN_MAP) -> None:
        super().__init__()
        self._color = color
        self._tile_size = 8
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
        surface = pg.Surface((len(self._map_data[0]) * self._tile_size, len(self._map_data) * self._tile_size))
        for y, row in enumerate(self._map_data):
            for x, tile in enumerate(row):
                surface.blit(self._tiles[tile - 1], (x * self._tile_size, y * self._tile_size))
        return surface

    def prerender_map_surface(self) -> Surface:
        return copy(self._image)

    def prerender_map_image_scaled(self) -> ImageObject:
        return ImageObject(self.prerender_map_surface())

    def draw(self, screen: Surface) -> None:
        screen.blit(self.surface_for_draw, (0, 20))
