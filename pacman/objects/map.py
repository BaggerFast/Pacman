from copy import copy
from random import randint

import pygame as pg

from pacman.data_core import Colors, PathManager
from pacman.misc.sprite_sheet import sprite_slice
from pacman.objects import DrawableObject, ImageObject


def rand_color():
    max_states = 7
    min_val = 200
    max_val = 230
    state = randint(0, max_states)
    if state == max_states:
        color = (255, 255, 255)
    elif state == max_states - 1:
        color = (randint(min_val, max_val), 0, 0)
    elif state == max_states - 2:
        color = (0, randint(min_val, max_val), 0)
    elif state == max_states - 3:
        color = (0, 0, randint(min_val, max_val))
    else:
        excluded_color = randint(0, 2)
        color = (
            randint(min_val, max_val) if excluded_color != 0 else 0,
            randint(min_val, max_val) if excluded_color != 1 else 0,
            randint(min_val, max_val) if excluded_color != 2 else 0,
        )
    return color


class Map(DrawableObject):
    def __init__(self, game, map_data) -> None:
        super().__init__()
        self.color = rand_color()
        self.game = game
        self.tile_size = 8
        self.map_data = map_data
        self.__size = (224, 248)
        self.surface = pg.Surface(self.__size)
        self.tiles = sprite_slice(
            pg.image.load(PathManager.get_image_path("map.png")), (self.tile_size, self.tile_size)
        )
        self.surface = self.__load_surface()
        self.surface_for_draw = self.__surface_recolor()

    def __surface_recolor(self) -> pg.Surface:
        srf = copy(self.surface)
        for x in range(srf.get_width()):
            for y in range(srf.get_height()):
                if srf.get_at((x, y)) == Colors.MAIN_MAP:
                    srf.set_at((x, y), self.color)
        return srf

    def __load_surface(self) -> pg.Surface:
        surface = pg.Surface((len(self.map_data[0]) * self.tile_size, len(self.map_data) * self.tile_size))
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                surface.blit(self.tiles[tile - 1], (x * self.tile_size, y * self.tile_size))
        return surface

    def prerender_map_surface(self) -> pg.Surface:
        return self.surface

    def prerender_map_image_scaled(self) -> ImageObject:
        image = ImageObject(self.game, self.prerender_map_surface(), (110, 96))
        return image

    def process_draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surface, (0, 20))
