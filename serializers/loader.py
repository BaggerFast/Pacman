import json
import os

from misc import PathManager
from serializers.serializers import JsonSerializer, JsonDeserializer


class BaseLoader:

    def __init__(self, storage, path: str):
        self._storage_filepath = PathManager.get_path(path)
        self._storage = storage


class SerializerLoader(BaseLoader):

    def serialize_obj(self) -> None:
        if not isinstance(self._storage, JsonSerializer):
            raise Exception(f'Попытка серилиазовать обьект {type(self._storage)}')

        try:
            os.mkdir(self._storage_filepath.split('/')[0])
        except FileExistsError:
            pass

        with open(self._storage_filepath, 'w') as f:
            f.write(json.dumps(self._storage.serialize(), indent=2))


class DeserializerLoader(BaseLoader):

    def deserialize_file(self) -> None:
        if not isinstance(self._storage, JsonDeserializer):
            raise Exception(f'Попытка десериализовать обьект {type(self._storage)}')
        if os.path.exists(self._storage_filepath):
            with open(self._storage_filepath, "r") as file:
                self._storage.deserialize(json.load(file))


class SerDesLoader(SerializerLoader, DeserializerLoader):

    def __init__(self, storage, path: str = 'saves/storage.json'):
        super().__init__(storage, path)





