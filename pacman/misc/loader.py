import json
import os


class SeedLoader:
    def __init__(self, data: json) -> None:
        self.__json = data
        self.__seeds = []
        self.__prepare_seeds()

    # region Public

    @property
    def seeds(self) -> list[list[bool]]:
        return self.__seeds

    @property
    def energizers(self) -> list[list[int]]:
        return self.__json["static_objects"]["big_dots"]

    # endregion

    # region Private

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

    # endregion


class LevelLoader:
    def __init__(self, file_name: str) -> None:
        self.__json = self.__load_map_json(file_name)
        self.__seed_loader = SeedLoader(self.__json)

    @property
    def map(self) -> list[list[int]]:
        return self.__json["map"]

    @property
    def collision_map(self) -> list[list[int]]:
        return self.__json["collision_map"]

    @property
    def seeds_map(self) -> list[list[bool]]:
        return self.__seed_loader.seeds

    @property
    def energizers_pos(self) -> list[list[int]]:
        return self.__seed_loader.energizers

    @property
    def heros_pos(self):
        return self.__json["characters"]

    @property
    def fruit_pos(self):
        return self.__json["static_objects"]["fruit"]

    @property
    def slow_ghost_rect(self):
        return self.__json["rects"]["slow_zone"]

    @staticmethod
    def __load_map_json(file_name) -> json:
        with open(os.path.join("maps", file_name)) as f:
            return json.load(f)
