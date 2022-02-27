import json

from misc import create_file_if_not_exist, get_path
from misc.constants import HIGHSCORES_COUNT, FRUITS_COUNT
from misc.constants.skin_names import SkinsNames


class Field:
    def dict(self):
        data = {}
        for key in self.__dict__.keys():
            if key == 'game':
                continue
            if hasattr(self.__dict__[key], 'dict'):
                data[key] = self.__dict__[key].dict()
            else:
                if hasattr(self.__dict__[key], '__dict__') and not key.startswith('_'):
                    data[key] = self.__dict__[key].__dict__
                else:
                    data[key] = self.__dict__[key]
        return data

    def read_dict(self, value):
        for key in self.__dict__.keys():
            if key in value.keys():
                if hasattr(self.__dict__[key], 'dict'):
                    self.__dict__[key].read_dict(value[key])
                else:
                    self.__dict__[key] = value[key]


class Storage(Field):
    class __Settings(Field):
        def __init__(self):
            self.SOUND = True
            self.FUN = False
            self.VOLUME = 100
            self.DIFFICULTY = 0

    __storage_filepath = get_path('saves/storage.json')

    def __init__(self, game) -> None:
        self.game = game
        # todo delete game
        self.last_level_id = 0
        self.last_skin = SkinsNames.default
        self.unlocked_levels = [0]
        self.unlocked_skins = [SkinsNames.default]
        self.settings = self.__Settings()
        self.eaten_fruits = [0] * FRUITS_COUNT
        self.highscores = [[0 for _ in range(HIGHSCORES_COUNT)] for _ in range(len(game.maps))]
        self.load()

    def save(self) -> None:
        self.settings.SOUND = self.game.settings.SOUND
        self.settings.FUN = self.game.settings.FUN
        self.settings.VOLUME = self.game.settings.VOLUME
        self.settings.DIFFICULTY = self.game.settings.DIFFICULTY
        self.last_level_id = self.game.maps.cur_id
        self.last_skin = self.game.skins.current.name
        self.eaten_fruits = self.game.eaten_fruits

        self.unlocked_levels = self.unlocked_levels if not self.game.cheats_var.UNLOCK_LEVELS else self.game.storage.unlocked_levels
        self.unlocked_skins = self.unlocked_skins if not self.game.cheats_var.UNLOCK_SKINS else self.game.storage.unlocked_skins

        self.highscores = self.game.highscores
        self.save_to_file()

    def save_to_file(self):
        string = json.dumps(self.dict(), indent=2)
        with open(self.__storage_filepath, "w") as file:
            file.write(string)

    def load(self) -> None:
        create_file_if_not_exist(self.__storage_filepath, json.dumps(self.dict(), indent=2))
        with open(self.__storage_filepath, "r") as file:
            self.read_dict(json.load(file))
