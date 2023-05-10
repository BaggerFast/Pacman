import json
import os
from copy import deepcopy
from typing import List, Tuple


class SeedLoader:
    def __init__(self, data) -> None:
        self.__json = data
        self.__seeds = []
        self.__prepare_seeds()

    @property
    def seeds(self) -> List[bool]:
        return self.__seeds

    @property
    def energizers(self) -> List[Tuple[int, int]]:
        return self.__json["static_objects"]["big_dots"]

    def __prepare_seeds(self) -> None:
        self.__seeds = [[bool(x) for x in y] for y in self.__json["collision_map"]]
        self.__remove_seeds_under_fruit()
        self.__remove_seeds_under_pacman()
        self.__remove_seeds_under_ghosts()
        self.__remove_seeds_under_energizers()

    def __remove_seeds_under_fruit(self) -> None:
        fruit_y = self.__json["static_objects"]["fruit"][1]
        fruit_x = self.__json["static_objects"]["fruit"][0]
        self.__seeds[fruit_y][int(fruit_x - 0.5)] = False
        self.__seeds[fruit_y][int(fruit_x + 0.5)] = False

    def __remove_seeds_under_pacman(self) -> None:
        player_y = self.__json["characters"]["pacman"][1]
        player_x = self.__json["characters"]["pacman"][0]
        self.__seeds[player_y][int(player_x - 0.5)] = False
        self.__seeds[player_y][int(player_x + 0.5)] = False

    def __remove_seeds_under_ghosts(self) -> None:
        for i in self.__json["rects"]["no_dots"]:
            for y in range(i[1], i[3] + 1):
                for x in range(i[0], i[2] + 1):
                    self.__seeds[y][x] = False

    def __remove_seeds_under_energizers(self) -> None:
        for x, y in self.__json["static_objects"]["big_dots"]:
            self.__seeds[y][x] = False


class LevelLoader:
    def __init__(self, file_name: str) -> None:
        self.__json = self.__load_map_json(file_name)
        self.__seed_loader = SeedLoader(self.__json)

    @staticmethod
    def __load_map_json(file_name) -> dict:
        with open(os.path.join("maps", file_name)) as f:
            return json.load(f)

    @property
    def map(self) -> List[List[int]]:
        return self.__json["map"]

    @property
    def collision_map(self) -> List[List[int]]:
        return self.__json["collision_map"]

    @property
    def seeds_map(self) -> List[bool]:
        return self.__seed_loader.seeds

    @property
    def energizers_pos(self) -> List[Tuple[int, int]]:
        return self.__seed_loader.energizers

    @property
    def heros_pos(self):
        return self.__json["characters"]

    @property
    def fruit_pos(self) -> Tuple[float, float]:
        return self.__json["static_objects"]["fruit"]

    @property
    def slow_ghost_rect(self):
        return self.__json["rects"]["slow_zone"]
