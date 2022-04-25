import json
import os
from misc import PathManager
from misc.constants import HIGHSCORES_COUNT
from misc.constants.skin_names import SkinsNames
from misc.serializers.modules import SerializerField, SettingsSerializer, EatenFruitsSerializer


class Storage(SerializerField):

    __storage_filepath = PathManager.get_path('saves/storage.json')

    def __init__(self, game) -> None:
        # todo delete game
        self.last_level_id = 0
        self.last_skin = SkinsNames.default
        # self.levels = [{0: []}]
        self.unlocked_levels = [0]
        self.highscores = [[0 for _ in range(HIGHSCORES_COUNT)] for _ in range(len(game.maps))]

        self.unlocked_skins = [SkinsNames.default]
        self.settings = SettingsSerializer()
        self.eaten_fruits = EatenFruitsSerializer()
        self.load_from_file()

    # region Public

    def save(self, game) -> None:
        self.settings.SOUND = game.settings.SOUND
        self.settings.FUN = game.settings.FUN
        self.settings.VOLUME = game.settings.VOLUME
        self.settings.DIFFICULTY = game.settings.DIFFICULTY
        self.last_level_id = game.maps.cur_id
        self.last_skin = game.skins.current.name
        self.eaten_fruits = game.eaten_fruits

        self.unlocked_levels = self.unlocked_levels if not game.cheats_var.UNLOCK_LEVELS \
            else game.storage.unlocked_levels
        self.unlocked_skins = self.unlocked_skins if not game.cheats_var.UNLOCK_SKINS \
            else game.storage.unlocked_skins

        self.highscores = game.highscores
        self.save_to_file()

    # todo separation of logic
    def save_to_file(self):
        string = json.dumps(self.serialize_to_dict(), indent=2)
        with open(self.__storage_filepath, "w") as file:
            file.write(string)

    def load_from_file(self) -> None:
        if os.path.exists(self.__storage_filepath):
            with open(self.__storage_filepath, "r") as file:
                self.deserialize_from_dict(json.load(file))
            return
        with open(self.__storage_filepath, 'w') as f:
            f.write(json.dumps(self.serialize_to_dict(), indent=2))
    # endregion
