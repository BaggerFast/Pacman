import json
import os


class SeedLoader:
    def __init__(self, data):
        self.__json = data
        self.seeds = []
        self.prepare_seeds()

    def remove_seeds_under_ghost_area(self):
        for i in self.__json["not_dots_rect"]:
            for y in range(i[1], i[3] + 1):
                for x in range(i[0], i[2] + 1):
                    self.seeds[y][x] = False

    def remove_seeds_under_pacman(self):
        self.seeds[self.__json["player_pos"][1]][int(self.__json["player_pos"][0] - 0.5)] = False
        self.seeds[self.__json["player_pos"][1]][int(self.__json["player_pos"][0] + 0.5)] = False

    def remove_seeds_under_energizers(self):
        for i in self.__json["big_dots_pos"]:
            self.seeds[i[1]][i[0]] = False

    def prepare_seeds(self):
        self.seeds = [[bool(x) for x in y] for y in self.__json["collision_map"]]
        self.remove_seeds_under_ghost_area()
        self.remove_seeds_under_pacman()
        self.remove_seeds_under_energizers()

    def get_seed_data(self):
        return self.seeds

    def get_energizer_data(self):
        return self.__json["big_dots_pos"]


class LevelLoader:
    def __init__(self, filename="original.map"):
        self.filename = filename
        self.__load_map_json()
        self.movements_map = self.get_movements_data()
        self.seed_loader = SeedLoader(self.__json)
        self.seed_data = self.seed_loader.get_seed_data()
        self.energizer_data = self.seed_loader.get_energizer_data()

    def __load_map_json(self):
        with open(os.path.join('maps', 'map.json')) as f:
            self.__json = json.load(f)

    def get_map_data(self):
        return self.__json['map']

    def get_movements_data(self):
        return self.__json["collision_map"]

    def get_seed_data(self):
        return self.seed_loader.get_seed_data()

    def get_energizer_data(self):
        return self.seed_loader.get_energizer_data()

    def get_player_position(self):
        return self.__json["player_pos"]

    def get_ghost_positions(self):
        return self.__json["ghosts_pos"]

    def get_fruit_position(self):
        return self.__json["fruit_pos"]