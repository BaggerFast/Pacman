import json
import pygame
import zipfile
import os


def get_maps_list():
    return [i[:-4] for i in os.listdir("maps/")]


def load_map(name):
    return Map(map_file=name)


class Map:
    def __init__(self, map_file="test.map"):
        with zipfile.ZipFile("maps/" + map_file + ".map") as archive:
            with archive.open("map.json") as f:
                loaded_map = json.load(f)
                pass
            self.surface = pygame.Surface((224, 248))
            loaded_map["tiles"] = \
                [pygame.image.load(archive.open("tiles/" + i)) for i in
                 loaded_map["tiles"]]
            self.start_player_pos = loaded_map["player_pos"]
            self.start_ghost_start_pos = loaded_map["ghosts_pos"]
            if len(self.start_ghost_start_pos) != 4:
                raise ValueError("Некорректное количество призраков в файле карты")
            for y in range(len(loaded_map["map"])):
                for x in range(len(loaded_map["map"][y])):
                    temp_surface = loaded_map["tiles"][loaded_map["map"][y][x][0]]
                    if len(loaded_map["map"][y][x])==2:
                        temp_surface = pygame.transform.flip(temp_surface,
                                                             loaded_map["map"][y][x][1]
                                                             // 4, False)
                        temp_surface = pygame.transform.rotate(temp_surface,
                                                               loaded_map["map"][y][x][1]
                                                               % 4 * -90)
                    self.surface.blit(temp_surface, (x * 8, y * 8)) # поверхность картинки карты
            self.collision_map = loaded_map["collision_map"]
            #  колизия 1 - вправо можно, 2 - вниз , 4 - влево, 8 - вверх
            # 9 = 1 + 8 можно вверх и вправо


def map_test():
    print("\nMap list")
    for i in get_maps_list():
        print('  ' + i)
    map_name = input("\nВведите название карты: ")
    pygame.display.init()
    pygame.display.set_mode((224, 248), flags=pygame.SCALED).blit(
        load_map(map_name).surface, (0, 0))
    pygame.display.flip()
    while not sum([i.type == pygame.QUIT for i in pygame.event.get()]):
        pass
    pygame.display.quit()


if __name__ == "__main__":
    map_test()
