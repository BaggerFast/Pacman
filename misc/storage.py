import json
import os
from json import JSONDecodeError

from misc import ROOT_DIR, create_file_if_not_exist, FRUITS_COUNT, HIGHSCORES_COUNT


class Storage:
    __storage_filepath = os.path.join(ROOT_DIR, "saves", "storage.json")

    def __init__(self, game) -> None:
        self.last_level_id = 0
        self.last_skin = "default"
        self.unlocked_levels = [0]
        self.unlocked_skins = ["default"]
        self.eaten_fruits = [0 for _ in range(FRUITS_COUNT)]
        self.highscores = [[0 for _ in range(HIGHSCORES_COUNT)] for _ in range(game.maps.count)]
        self.create_settings(game)
        self.load()

    def create_settings(self, game):
        self.settings = {}
        data = set(vars(game.Settings).keys())
        for i in data:
            if i.isupper():
                self.settings[i] = False
        print(self.settings)

    def save(self) -> None:
        string = json.dumps(self.__dict__)
        with open(self.__storage_filepath, "w") as file:
            file.write(string)

    def load(self) -> None:
        create_file_if_not_exist(self.__storage_filepath, json.dumps(self.__dict__))
        with open(self.__storage_filepath, "r") as file:
            try:
                json_dict = json.load(file)
                for key in self.__dict__.keys():
                    if key in json_dict:
                        self.__dict__[key] = json_dict[key]
            except JSONDecodeError:
                pass
        self.save()

