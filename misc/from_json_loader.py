from typing import List, Tuple
from .base_from_file_loader import BaseFromFileLoader
from .constants import CELL_SIZE
from .vec import Vec
from .rotation import Rotation
from .path import get_path
import json
import os

import pygame as pg


class FromJsonLoader(BaseFromFileLoader):
    tile_names = [
        "space",
        "fat_up_wall", "fat_left_corner",
        "fat_y_corner", "up_wall",
        "left_corner", "ghost_left_corner",
        "ghost_door", "ghost_door_wall_left"
    ]
    tiles = []

    for name in tile_names:
        tiles.append(pg.image.load(get_path(name, 'png', 'images', 'map')))

    def __init__(self, filename: str):
        self.json: dict = {}
        self.map_data: List[List[Tuple[int, int]]] = \
            [[(0, 0) for _ in range(self.size[0])]for _ in range(self.size[1])]
        self.tile_data: List[pg.Surface] = []
        self.not_dots_rect: List[Tuple[int, int, int, int]] = []
        super().__init__(filename)

    def load(self):
        self.__load_json()
        self.__load_player_position()
        self.__load_ghosts_position()
        self.__load_fruit_position()
        self.__load_energizers_position()
        self.__load_not_dots_rect()
        self.__load_slow_ghost_rect()
        self.__load_cant_up_ghost_rect()
        self.__load_movement_data()
        self.__load_map_data()
        self.__create_seed_map()
        self.__render_map_surface()

    def __load_json(self):
        with open(os.path.join('maps', self.filename)) as f:
            self.json = json.load(f)

    def __load_player_position(self): self.player_pos = Vec(*self.json["player_pos"])
    def __load_ghosts_position(self): self.ghosts_pos = [Vec(*pos) for pos in self.json["ghosts_pos"]]
    def __load_fruit_position(self): self.fruit_pos = Vec(*self.json["fruit_pos"])
    def __load_energizers_position(self): self.energizers_pos = [Vec(*pos) for pos in self.json["big_dots_pos"]]
    def __load_not_dots_rect(self): self.not_dots_rect = [tuple(rect) for rect in self.json["not_dots_rect"]]
    def __load_slow_ghost_rect(self): self.slow_ghost_rect = [tuple(rect) for rect in self.json["slow_ghost_rect"]]

    def __load_cant_up_ghost_rect(self):
        self.cant_up_ghost_rect = [pg.Rect(rect) for rect in self.json["cant_up_ghost_rect"]]

    def __load_movement_data(self): self.movements_data = self.json["collision_map"]

    def __load_map_data(self):
        self.map_data = self.json["map"]
        for line in self.map_data:
            for i, tile in enumerate(line):
                line[i] = tuple(tile)

    def __create_seed_map(self):
        self.seed_data = [[True for _ in range(self.size[0])]for _ in range(self.size[1])]

        for x, y in self.size.iterator_to((0, 0)):
            if not self.movements_data[y][x]:
                self.seed_data[y][x] = False

        for rect in self.not_dots_rect:
            for x, y in (Vec(rect[2], rect[3]) + (1, 1)).iterator_to((rect[0], rect[1])):
                self.seed_data[y][x] = False

        self.seed_data[int(self.player_pos[1])][int(self.player_pos[0])] = False
        self.seed_data[int(self.player_pos[1])][int(self.player_pos[0])+1] = False

        self.seed_data[int(self.fruit_pos[1])][int(self.fruit_pos[0])] = False
        self.seed_data[int(self.fruit_pos[1])][int(self.fruit_pos[0])+1] = False

        for pos in self.ghosts_pos:
            self.seed_data[int(pos[1])][int(pos[0])] = False

        for pos in self.energizers_pos:
            self.seed_data[int(pos[1])][int(pos[0])] = False

    def __corner_preprocess(self, x, y, temp_surface: pg.Surface) -> pg.Surface:
        flip_x = bool(self.map_data[y][x][1] // len(Rotation))
        flip_y = False
        temp_surface = pg.transform.flip(temp_surface, flip_x, flip_y)
        rotate_angle = self.map_data[y][x][1] % len(Rotation) * -90
        temp_surface = pg.transform.rotate(temp_surface, rotate_angle)
        return temp_surface

    def __draw_cell(self, x, y):
        temp_surface = self.tiles[self.map_data[y][x][0]]
        if len(self.map_data[y][x]) == 2:
            temp_surface = self.__corner_preprocess(x, y, temp_surface)
        self.surface.blit(temp_surface, (x * CELL_SIZE, y * CELL_SIZE))

    def __render_map_surface(self):
        for x, y in Vec(0, 0).iterator_to(self.size):
            self.__draw_cell(x, y)

    def clear_memory(self):
        self.json = None
        self.map_data = None
        self.not_dots_rect = None
