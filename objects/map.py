import pygame
import os

from misc.path import get_image_path
from objects.base import DrawableObject


class Map(DrawableObject):
    tile_names = [
        "space.png",
        "fat_up_wall.png", "fat_left_corner.png",
        "fat_y_corner.png", "out_corner.png",
        "up_wall.png", "left_corner.png",
        "ghost_up_wall.png", "ghost_left_corner.png",
        "ghost_door.png", "ghost_door_wall_left.png"
    ]
    tiles = []

    def __init__(self, game, map_data, x=0, y=20):
        super().__init__(game)
        self.x = x
        self.y = y
        self.map = map_data
        self.surface = pygame.Surface((224, 248))
        self.__load_tiles()
        self.__render_map_surface()

    def __load_tiles(self):
        self.tiles = []
        for i in self.tile_names:
            tile_path = get_image_path(os.path.join("map", i))
            tile = pygame.image.load(tile_path)
            self.tiles.append(tile)

    def __corner_preprocess(self, x, y, temp_surface):
        flip_x = self.map[y][x][1] // 4
        flip_y = False
        temp_surface = pygame.transform.flip(temp_surface, flip_x, flip_y)
        rotate_angle = self.map[y][x][1] % 4 * -90
        temp_surface = pygame.transform.rotate(temp_surface, rotate_angle)
        return temp_surface

    def __draw_cell(self, x, y):
        temp_surface = self.tiles[self.map[y][x][0]]
        if len(self.map[y][x]) == 2:
            temp_surface = self.__corner_preprocess(x, y, temp_surface)
        self.surface.blit(temp_surface, (x * 8, y * 8))

    def __render_map_surface(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                self.__draw_cell(x, y)

    def process_draw(self):
        self.game.screen.blit(self.surface, (self.x, self.y))
