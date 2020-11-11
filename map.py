import json
import pygame
import zipfile


class Map:
    def __init__(self, map_file="test.map"):
        with zipfile.ZipFile("maps/" + map_file) as archive:
            with archive.open("map.json") as f:
                load_map = json.load(f)
                pass
            self.surface = pygame.Surface((224, 264))
            load_map["tiles"] = \
                [pygame.image.load(archive.open("tiles/" + i)) for i in
                 load_map["tiles"]]
            self.start_player_pos = load_map["player_pos"]
            self.start_ghost_start_pos = load_map["ghosts_pos"]
            if len(self.start_ghost_start_pos) != 4:
                raise ValueError("Некорректное количество призраков в файле карты")
            for y in range(len(load_map["map"])):
                for x in range(len(load_map["map"][y])):
                    temp_surface = load_map["tiles"][load_map["map"][y][x][0]]
                    temp_surface = pygame.transform.flip(temp_surface,
                                                         load_map["map"][y][x][1]
                                                         // 4, False)
                    temp_surface = pygame.transform.rotate(temp_surface,
                                                           load_map["map"][y][x][1]
                                                           % 4 * -90)
                    self.surface.blit(temp_surface, (x * 8, y * 8))
            self.collision_map = load_map["collision_map"]


if __name__ == "__main__":
    pygame.display.init()
    pygame.display.set_mode((224, 264), flags=pygame.SCALED).blit((Map().surface), (0, 0))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.display.quit()
