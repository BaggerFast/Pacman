import json
import os
from misc import PathManager
from serializers.serializers import BaseSerializer


class SerializerLoader:

    def __init__(self, storage: BaseSerializer, path: str = 'saves/storage.json'):
        self.__storage_filepath = PathManager.get_path(path)
        self.__storage = storage

    def save_to_file(self) -> None:
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
