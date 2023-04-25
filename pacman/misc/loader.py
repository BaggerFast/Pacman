import json
import os
from copy import deepcopy
from typing import List, Tuple


class SeedLoader:
    def __init__(self, data) -> None:
        self.__json = data
        self.__seeds = []
        self.__prepare_seeds()

    def __remove_seeds_under_fruit(self) -> None:
        fruit_y = self.__json["fruit_pos"][1]
        fruit_x = self.__json["fruit_pos"][0]
        self.__seeds[fruit_y][int(fruit_x - 0.5)] = False
        self.__seeds[fruit_y][int(fruit_x + 0.5)] = False

    def __remove_seeds_under_pacman(self) -> None:
        player_y = self.__json["characters"]["pacman"][1]
        player_x = self.__json["characters"]["pacman"][0]
        self.__seeds[player_y][int(player_x - 0.5)] = False
        self.__seeds[player_y][int(player_x + 0.5)] = False

    def __remove_seeds_under_energizers(self) -> None:
        for x, y in self.__json["big_dots_pos"]:
            self.__seeds[y][x] = False

    def __remove_seeds_under_ghost_area(self) -> None:
        for i in self.__json["not_dots_rect"]:
            for y in range(i[1], i[3] + 1):
                for x in range(i[0], i[2] + 1):
                    self.__seeds[y][x] = False

    def __prepare_seeds(self) -> None:
        self.__seeds = [[bool(x) for x in y] for y in self.__json["collision_map"]]
        self.__remove_seeds_under_ghost_area()
        self.__remove_seeds_under_pacman()
        self.__remove_seeds_under_fruit()
        self.__remove_seeds_under_energizers()

    def get_seed_data(self) -> List[bool]:
        return deepcopy(self.__seeds)

    def get_energizer_data(self) -> List[Tuple[int, int]]:
        return deepcopy(self.__json["big_dots_pos"])


class LevelLoader:
    def __init__(self, filename="1_map.json") -> None:
        self.filename = filename
        self.__load_map_json()
        self.movements_map = self.get_movements_data()
        self.__seed_loader = SeedLoader(self.__json)

    def __load_map_json(self) -> None:
        with open(os.path.join("maps", self.filename)) as f:
            self.__json = json.load(f)

    def get_map_data(self) -> List[List[int]]:
        return deepcopy(self.__json["map"])

    def get_movements_data(self) -> List[List[int]]:
        return deepcopy(self.__json["collision_map"])

    def get_seed_data(self) -> List[bool]:
        return self.__seed_loader.get_seed_data()

    def get_energizer_data(self) -> List[Tuple[int, int]]:
        return self.__seed_loader.get_energizer_data()

    def get_hero_postions(self):
        return deepcopy(self.__json["characters"])

    def get_fruit_position(self) -> Tuple[int | float, int | float]:
        return deepcopy(self.__json["fruit_pos"])

    def get_slow_ghost_rect(self):
        return deepcopy(self.__json["slow_ghost_rect"])

    def get_cant_up_ghost_rect(self):
        return deepcopy(self.__json["cant_up_ghost_rect"])
