import json
import os
from typing import List, Tuple, Union


class SeedLoader:
    def __init__(self, data) -> None:
        self.__json = data
        self.__seeds = []
        self.__prepare_seeds()

    def __remove_seeds_under_ghost_area(self) -> None:
        for i in self.__json["not_dots_rect"]:
            for y in range(i[1], i[3] + 1):
                for x in range(i[0], i[2] + 1):
                    self.__seeds[y][x] = False

    def __remove_seeds_under_pacman(self) -> None:
        self.__seeds[self.__json["player_pos"][1]][int(self.__json["player_pos"][0] - 0.5)] = False
        self.__seeds[self.__json["player_pos"][1]][int(self.__json["player_pos"][0] + 0.5)] = False

    def __remove_seeds_under_fruit(self) -> None:
        self.__seeds[self.__json["fruit_pos"][1]][int(self.__json["fruit_pos"][0] - 0.5)] = False
        self.__seeds[self.__json["fruit_pos"][1]][int(self.__json["fruit_pos"][0] + 0.5)] = False

    def __remove_seeds_under_energizers(self) -> None:
        for i in self.__json["big_dots_pos"]:
            self.__seeds[i[1]][i[0]] = False

    def __prepare_seeds(self) -> None:
        self.__seeds = [[bool(x) for x in y] for y in self.__json["collision_map"]]
        self.__remove_seeds_under_ghost_area()
        self.__remove_seeds_under_pacman()
        self.__remove_seeds_under_fruit()
        self.__remove_seeds_under_energizers()

    def get_seed_data(self) -> List[bool]:
        return self.__seeds

    def get_energizer_data(self) -> List[Tuple[int, int]]:
        return self.__json["big_dots_pos"]


class LevelLoader:
    def __init__(self, filename="1_map.json") -> None:
        self.filename = filename
        self.__load_map_json()
        self.movements_map = self.get_movements_data()
        self.__seed_loader = SeedLoader(self.__json)
        self.__seed_data = self.__seed_loader.get_seed_data()
        self.energizer_data = self.__seed_loader.get_energizer_data()

    def __load_map_json(self) -> None:
        with open(os.path.join('maps', self.filename)) as f:
            self.__json = json.load(f)

    def get_map_data(self) -> List[List[List[int]]]:
        return self.__json["map"]

    def get_movements_data(self) -> List[List[int]]:
        return self.__json["collision_map"]

    def get_seed_data(self) -> List[bool]:
        return self.__seed_loader.get_seed_data()

    def get_energizer_data(self) -> List[Tuple[int, int]]:
        return self.__seed_loader.get_energizer_data()

    def get_player_position(self) -> Tuple[Union[int, float], Union[int, float]]:
        return self.__json["player_pos"]

    def get_ghost_positions(self) -> List[Tuple[Union[int, float], Union[int, float]]]:
        return self.__json["ghosts_pos"]

    def get_fruit_position(self) -> Tuple[Union[int, float], Union[int, float]]:
        return self.__json["fruit_pos"]

    def get_slow_ghost_rect(self):
        return self.__json["slow_ghost_rect"]

    def get_cant_up_ghost_rect(self):
        return self.__json["cant_up_ghost_rect"]
