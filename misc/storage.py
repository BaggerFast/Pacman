import json
from misc import create_file_if_not_exist, get_path
from misc.constants import HIGHSCORES_COUNT, FRUITS_COUNT
from misc.constants.skin_names import SkinsNames


class JsonField:

    # region Public

    def serialization_to_dict(self):
        data = {}
        for key in self.__dict__:
            if isinstance(self.__dict__[key], JsonField):
                data[key] = self.__dict__[key].serialization_to_dict()
            elif not key.startswith('_'):
                data[key] = self.__dict__[key]
        return data

    def sync_with_dict(self, value: dict):
        for key in self.__dict__:
            if key not in value:
                continue
            if isinstance(self.__dict__[key], JsonField):
                self.__dict__[key].sync_with_dict(value[key])
            else:
                self.__dict__[key] = value[key]

    # endregion


class Storage(JsonField):
    class __Settings(JsonField):
        def __init__(self):
            self.SOUND = True
            self.FUN = False
            self.VOLUME = 100
            self.DIFFICULTY = 0

    __storage_filepath = get_path('saves/storage.json')

    def __init__(self, game) -> None:
        self.__game = game
        # todo delete game
        self.last_level_id = 0
        self.last_skin = SkinsNames.default
        self.unlocked_levels = [0]
        self.unlocked_skins = [SkinsNames.default]
        self.settings = self.__Settings()
        self.eaten_fruits = [0] * FRUITS_COUNT
        self.highscores = [[0 for _ in range(HIGHSCORES_COUNT)] for _ in range(len(game.maps))]
        self.load()

    # region Public

    def save(self) -> None:
        self.settings.SOUND = self.__game.settings.SOUND
        self.settings.FUN = self.__game.settings.FUN
        self.settings.VOLUME = self.__game.settings.VOLUME
        self.settings.DIFFICULTY = self.__game.settings.DIFFICULTY
        self.last_level_id = self.__game.maps.cur_id
        self.last_skin = self.__game.skins.current.name
        self.eaten_fruits = self.__game.eaten_fruits

        self.unlocked_levels = self.unlocked_levels if not self.__game.cheats_var.UNLOCK_LEVELS \
            else self.__game.storage.unlocked_levels
        self.unlocked_skins = self.unlocked_skins if not self.__game.cheats_var.UNLOCK_SKINS \
            else self.__game.storage.unlocked_skins

        self.highscores = self.__game.highscores
        self.save_to_file()

    def save_to_file(self):
        string = json.dumps(self.serialization_to_dict(), indent=2)
        with open(self.__storage_filepath, "w") as file:
            file.write(string)

    def load(self) -> None:
        create_file_if_not_exist(self.__storage_filepath, json.dumps(self.serialization_to_dict(), indent=2))
        with open(self.__storage_filepath, "r") as file:
            self.sync_with_dict(json.load(file))

    # endregion
