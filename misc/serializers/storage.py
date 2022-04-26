import json
import os
from misc import PathManager
from misc.serializers.modules import SerializerField, SettingsSerializer, EatenFruitsSerializer, LastSerializer, \
    UnlockedSerializer


# todo reformat module

class Storage(SerializerField):

    def __init__(self, game) -> None:
        self.settings = SettingsSerializer()
        self.eaten_fruits = EatenFruitsSerializer()
        self.last = LastSerializer()
        self.unlocked = UnlockedSerializer()


class StorageSetup:

    def __init__(self, storage: SerializerField, path: str = 'saves/storage.json'):
        self.__storage_filepath = PathManager.get_path(path)
        self.__storage = storage

    def save_to_file(self):
        string = json.dumps(self.__storage.serialize_to_dict(), indent=2)
        with open(self.__storage_filepath, "w") as file:
            file.write(string)

    def load_from_file(self) -> None:
        if os.path.exists(self.__storage_filepath):
            with open(self.__storage_filepath, "r") as file:
                self.__storage.deserialize_from_dict(json.load(file))
            return
        with open(self.__storage_filepath, 'w') as f:
            f.write(json.dumps(self.__storage.serialize_to_dict(), indent=2))
