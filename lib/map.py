import json
import pygame
import zipfile
import os

__all__ = ["get_maps_list", "load_map"]


def get_maps_list():
    return [i[:-4] for i in os.listdir("maps/")]


def load_map(name="original"):
    map = Map(map_file=name)
    return {"map_name": name, "surface": map.surface,
            "player_pos": map.player_pos, "ghost_pos": map.ghost_pos,
            "collision": map.collision, "dots": map.dots,
            "big_dots": map.big_dots, "fruit_pos": map.fruit_pos}


class Map:
    def __init__(self, map_file="original"):
        self.map_name = map_file
        self.surface = pygame.Surface((224, 248))
        self.player_pos = None
        self.ghost_pos = None
        self.collision = None
        self.dots = None
        self.big_dots = None
        self.fruit_pos = None

        self.__file_open()
        self.__load_tiles()
        self.__load_surface()
        self.__load()
        self.__file_close()

    def __file_open(self):
        self.__archive = zipfile.ZipFile("maps/" + self.map_name + ".map")
        temp = self.__archive.open("map.json")
        self.__json = json.load(temp)
        temp.close()

    def __load_tiles(self):
        self.__json["tiles"] = \
            [pygame.image.load(self.__archive.open("tiles/" + i)) for i in
             self.__json["tiles"]]

    def __load_surface(self):
        for y in range(len(self.__json["map"])):
            for x in range(len(self.__json["map"][y])):
                temp_surface = self.__json["tiles"][
                    self.__json["map"][y][x][0]]
                if len(self.__json["map"][y][x]) == 2:
                    temp_surface = pygame.transform.flip(
                        temp_surface, self.__json["map"][y][x][1] // 4, False)
                    temp_surface = pygame.transform.rotate(
                        temp_surface, self.__json["map"][y][x][1] % 4 * -90)
                self.surface.blit(temp_surface, (x * 8, y * 8))

    def __load(self):
        self.player_pos = self.__json["player_pos"]
        self.ghost_pos = self.__json["ghosts_pos"]
        self.collision = self.__json["collision_map"]
        #  колизия 1 - вправо можно, 2 - вниз , 4 - влево, 8 - вверх
        # 9 = 1 + 8 можно вверх и вправо

        self.dots = [[bool(x) for x in y] for y in self.collision]
        for i in self.__json["not_dots_rect"]:
            for y in range(i[1], i[3] + 1):
                for x in range(i[0], i[2] + 1):
                    self.dots[y][x] = False
        # Загрузка зерна
        self.dots[self.player_pos[1]][int(self.player_pos[0] - 0.5)] = False
        self.dots[self.player_pos[1]][int(self.player_pos[0] + 0.5)] = False
        # удаление точек с позиции пакмена
        self.big_dots = self.__json["big_dots_pos"]

        for i in self.big_dots: self.dots[i[1]][i[0]] = False

        self.fruit_pos = self.__json["fruit_pos"]

    def __file_close(self):
        self.__archive.close()
        del self.__json["tiles"]
        del self.__json


'''def map_test():
    print("\nMap list")
    for i in get_maps_list():
        print('  ' + i)
    map = load_map(input("\nВведите название карты: "))
    pygame.display.init()
    s = pygame.display.set_mode((224, 248), flags=pygame.SCALED)
    s.blit(map.surface, (0, 0))
    pygame.display.flip()
    for y in range(len(map.dots)):
        for x in range(len(map.dots[y])):
            if map.dots[y][x]:
                pygame.draw.circle(s, (255, 255, 255), (x * 8 + 4, y * 8 + 4),
                                   1)

    pygame.display.flip()
    pygame.draw.circle(s, (255, 255, 0),
                       (map.player_pos[0] * 8 + 4, map.player_pos[1] * 8 + 4),
                       8)
    pygame.display.flip()

    pygame.draw.circle(s, (255, 0, 0), (
        map.ghost_pos[0][0] * 8 + 4, map.ghost_pos[0][1] * 8 + 4), 8)
    pygame.draw.circle(s, (255, 0, 255), (
        map.ghost_pos[1][0] * 8 + 4, map.ghost_pos[1][1] * 8 + 4), 8)
    pygame.draw.circle(s, (0, 0, 255), (
        map.ghost_pos[2][0] * 8 + 4, map.ghost_pos[2][1] * 8 + 4), 8)
    pygame.draw.circle(s, (0, 255, 0), (
        map.ghost_pos[3][0] * 8 + 4, map.ghost_pos[3][1] * 8 + 4), 8)
    pygame.display.flip()

    for i in map.big_dots:
        pygame.draw.circle(s, (255, 255, 255), (i[0] * 8 + 4, i[1] * 8 + 4), 4)

    pygame.draw.circle(s, (255, 0, 0), (map.fruit_pos[0] * 8 + 4,
                                        map.fruit_pos[1] * 8 + 4), 4)
    pygame.display.flip()

    while not sum([i.type == pygame.QUIT for i in pygame.event.get()]):
        pass
    pygame.display.quit()


if __name__ == "__main__":
    map_test()'''
