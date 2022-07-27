import json
import os
from abc import ABC

from pacman.misc import PathManager
from pacman.serializers.ser import JsonSerializer, JsonDeserializer


class BaseLoader:

    def __init__(self, storage: JsonDeserializer | JsonSerializer, path: str):
        self._storage_filepath = PathManager.get_path(path)
        self._storage = storage


class SerializerLoader(BaseLoader, ABC):

    def __init__(self, storage: JsonSerializer, path: str):
        super().__init__(storage, path)

    def serialize_to_file(self) -> None:
        if not isinstance(self._storage, JsonSerializer):
            raise Exception(f'Попытка серилиазовать объект {type(self._storage)}')

        try:
            pass
        except FileExistsError:
            pass

        with open(self._storage_filepath, 'w') as f:
            f.write(json.dumps(self._storage.serialize(), indent=2))


class DeserializerLoader(BaseLoader, ABC):

    def __init__(self, storage: JsonDeserializer, path: str):
        super().__init__(storage, path)

    def deserialize_from_file(self) -> None:
        if not isinstance(self._storage, JsonDeserializer):
            raise Exception(f'Попытка десериализовать объект {type(self._storage)}')
        if os.path.exists(self._storage_filepath):
            with open(self._storage_filepath, "r") as file:
                self._storage.deserialize(json.load(file))


class SerDesLoader(SerializerLoader, DeserializerLoader, ABC):

    def __init__(self, storage: JsonDeserializer | JsonSerializer, path: str):
        super().__init__(storage, path)
