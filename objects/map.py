from copy import copy
from random import randint, choice
import pygame as pg

from misc import PathManager
from misc.constants import Color
from misc.interfaces import IDrawable
from misc.sprite_sheet import SpriteSheet
from objects import ImageObject


def rand_color():
    max_states = 7
    min_val = 200
    max_val = 230
    state = randint(0, max_states)
    data = [
        (255, 255, 255),
        (randint(min_val, max_val), 0, 0),
        (0, randint(min_val, max_val), 0),
        (0, 0, randint(min_val, max_val))
    ]
    for i, new_color in enumerate(data):
        if state == max_states - i:
            return new_color
    return [randint(min_val, max_val) if choice([0, 1]) != i else 0 for i in range(3)]


class Map(IDrawable):

    color = rand_color()

    def __init__(self, map_data):

        self.map_data = map_data
        self.tile_size = 8
        self.sprite_sheet = SpriteSheet(sprite_path=PathManager.get_image_path('map.png'), sprite_size=(self.tile_size,
                                                                                                        self.tile_size))
        self.surface = self.__load_surface()
        self.surface_for_draw = self.__surface_recolor()

    # region Public

    # region Implementation of IDrawable

    def process_draw(self, screen: pg.Surface):
        screen.blit(self.surface_for_draw, (0, 20))

    # endregion

    def __surface_recolor(self) -> pg.Surface:
        srf = copy(self.surface)
        for x in range(srf.get_width()):
            for y in range(srf.get_height()):
                if srf.get_at((x, y)) == Color.MAIN_MAP:
                    srf.set_at((x, y), Map.color)
        return srf

    def __load_surface(self) -> pg.Surface:
        surface = pg.Surface((len(self.map_data[0]) * self.tile_size, len(self.map_data) * self.tile_size))
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                surface.blit(self.sprite_sheet[0][tile - 1], (x * self.tile_size, y * self.tile_size))
        return surface

    def prerender_map_surface(self) -> pg.Surface:
        return self.surface

    def prerender_map_image_scaled(self) -> ImageObject:
        image = ImageObject(self.surface, (110, 96))
        image.smooth_scale(100, 100)
        return image

    # endregion
