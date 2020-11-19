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



# -----------OLD source---------------------
import json
from tempfile import TemporaryDirectory
import zipfile

class GameTemp:
    def __init__(self):
        self.screen = pygame.display.set_mode((224, 280), flags=pygame.SCALED)


class OldMap(DrawableObject):
    def __init__(self, game, filename="original.map", x=0, y=20):
        super().__init__(game)
        self.x = x
        self.y = y
        self.temporary_dir = TemporaryDirectory(prefix='pacman__')
        self.map_name = filename
        self.player_position = None
        self.ghost_positions = None
        self.movements_map = None
        self.seeds = None
        self.big_dots = None
        self.fruit_pos = None

        self.__unpack_archive()
        self.__load_map_json()
        self.__load()
        self.__file_close()

    def __unpack_archive(self):
        self.__archive = zipfile.ZipFile(os.path.join("maps", self.map_name))
        self.__archive.extractall(self.temporary_dir.name)
        self.__archive.close()

    def __load_map_json(self):
        temp = open(os.path.join(self.temporary_dir.name, "map.json"))
        self.__json = json.load(temp)
        temp.close()

    def __prepare_seeds(self):
        self.seeds = [[bool(x) for x in y] for y in self.movements_map]
        for i in self.__json["not_dots_rect"]:
            for y in range(i[1], i[3] + 1):
                for x in range(i[0], i[2] + 1):
                    self.seeds[y][x] = False

        # удаление точек с позиции пакмена
        self.seeds[self.player_position[1]][int(self.player_position[0] - 0.5)] = False
        self.seeds[self.player_position[1]][int(self.player_position[0] + 0.5)] = False

        self.big_dots = self.__json["big_dots_pos"]
        for i in self.big_dots:
            self.seeds[i[1]][i[0]] = False

    def __load(self):
        """колизия
          1 - можно двигаться вправо
          2 - можно двигаться вниз
          4 - можно двигаться влево
          8 - можно двигаться вверх
          например, 9 = 1 + 8 - можно двигаться вверх и вправо
        """
        self.player_position = self.__json["player_pos"]
        self.ghost_positions = self.__json["ghosts_pos"]
        self.movements_map = self.__json["collision_map"]

        self.__prepare_seeds()

        self.fruit_pos = self.__json["fruit_pos"]

    def __file_close(self):
        del self.__json["map"]
        del self.__json


def map_test():
    pygame.display.init()
    g = GameTemp()
    map = OldMap(g)
    s = g.screen
    pygame.display.flip()

    pygame.display.flip()
    pygame.draw.circle(s, (255, 255, 0), (map.player_position[0] * 8 + 4, 20 + map.player_position[1] * 8 + 4), 8)
    pygame.display.flip()

    pygame.draw.circle(s, (255, 0, 0), (map.ghost_positions[0][0] * 8 + 4, 20 + map.ghost_positions[0][1] * 8 + 4), 8)
    pygame.draw.circle(s, (255, 0, 255), (map.ghost_positions[1][0] * 8 + 4, 20 + map.ghost_positions[1][1] * 8 + 4), 8)
    pygame.draw.circle(s, (0, 0, 255), (map.ghost_positions[2][0] * 8 + 4, 20 + map.ghost_positions[2][1] * 8 + 4), 8)
    pygame.draw.circle(s, (0, 255, 0), (map.ghost_positions[3][0] * 8 + 4, 20 + map.ghost_positions[3][1] * 8 + 4), 8)
    pygame.display.flip()

    pygame.draw.circle(s, (255, 0, 0), (map.fruit_pos[0] * 8 + 4, 20 + map.fruit_pos[1] * 8 + 4), 4)
    pygame.display.flip()

    while not sum([i.type == pygame.QUIT for i in pygame.event.get()]):
        pass
    pygame.display.quit()


if __name__ == "__main__":
    map_test()


