import json
import os
import zipfile
from tempfile import TemporaryDirectory


def main():
    pass


if __name__ == '__main__':
    main()


class SeedLoader:
    def __init__(self, data):
        self.__json = data
        self.seeds = []
        self.prepare_seeds()

    def remove_seeds_undex_ghost_area(self):
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
        self.remove_seeds_undex_ghost_area()
        self.remove_seeds_under_pacman()
        self.remove_seeds_under_energizers()

    def get_seed_data(self):
        return self.seeds

    def get_energizer_data(self):
        return self.__json["big_dots_pos"]


class LevelLoader:
    def __init__(self, filename="original.map"):
        self.filename = filename
        self.temporary_dir = TemporaryDirectory(prefix='pacman__')
        self.__unpack_archive()
        self.__load_map_json()
        self.movements_map = self.get_movements_data()
        self.seed_loader = SeedLoader(self.__json)
        self.seed_data = self.seed_loader.get_seed_data()
        self.energizer_data = self.seed_loader.get_energizer_data()

    def __unpack_archive(self):
        self.__archive = zipfile.ZipFile(os.path.join("maps", self.filename))
        self.__archive.extractall(self.temporary_dir.name)
        self.__archive.close()

    def __load_map_json(self):
        temp = open(os.path.join(self.temporary_dir.name, "map.json"))
        self.__json = json.load(temp)
        temp.close()

    def get_map_data(self):
        return self.__json['map']

    def get_movements_data(self):
        return self.__json["collision_map"]

    def get_seed_data(self):
        return self.seed_loader.get_seed_data()

    def get_energizer_data(self):
        return self.seed_loader.get_energizer_data()

    def get_seeds_data(self):
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