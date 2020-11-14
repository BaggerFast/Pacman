import json
import pygame
import zipfile
import os

__all__ = ["get_maps_list", "load_map"]


def get_maps_list():
    return [i[:-4] for i in os.listdir("maps/")]


def load_map(name="original"):
    return Map(map_file=name)


class Map:
    def __init__(self, map_file="original"):
        with zipfile.ZipFile("maps/" + map_file + ".map") as archive:
            with archive.open("map.json") as f:
                loaded_map = json.load(f)
                pass
            self.surface = pygame.Surface((224, 248))
            loaded_map["tiles"] = \
                [pygame.image.load(archive.open("tiles/" + i)) for i in
                 loaded_map["tiles"]]
            self.player_pos = loaded_map["player_pos"]
            self.ghost_pos = loaded_map["ghosts_pos"]
            if len(self.ghost_pos) != 4:
                raise ValueError(
                    "Некорректное количество призраков в файле карты")
            for y in range(len(loaded_map["map"])):
                for x in range(len(loaded_map["map"][y])):
                    temp_surface = loaded_map["tiles"][
                        loaded_map["map"][y][x][0]]
                    if len(loaded_map["map"][y][x]) == 2:
                        temp_surface = pygame.transform.flip(temp_surface,
                                                             loaded_map["map"][
                                                                 y][x][1]
                                                             // 4, False)
                        temp_surface = pygame.transform.rotate(temp_surface,
                                                               loaded_map[
                                                                   "map"][y][x][
                                                                   1]
                                                               % 4 * -90)
                    self.surface.blit(temp_surface, (x * 8, y * 8))
                    # поверхность картинки карты
            self.collision = loaded_map["collision_map"]
            #  колизия 1 - вправо можно, 2 - вниз , 4 - влево, 8 - вверх
            # 9 = 1 + 8 можно вверх и вправо
            self.dots = [[bool(x) for x in y]
                         for y in self.collision]
            # ставит точки на все места где можно ходить
            for i in loaded_map["not_dots_rect"]:
                for y in range(i[1], i[3] + 1):
                    for x in range(i[0], i[2] + 1):
                        self.dots[y][x] = False
            self.dots[self.player_pos[1]][int(self.player_pos[0] - 0.5)] = False
            self.dots[self.player_pos[1]][int(self.player_pos[0] + 0.5)] = False
            # удаление точек с позиции пакмена
            self.big_dots = loaded_map["big_dots_pos"]
            self.fruit_pos = loaded_map["fruit_pos"]


def map_test():
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
    map_test()
