import json
import os

from misc import PathManager
from misc.patterns import Singleton


class JsonSerializer:

    def serialize(self) -> dict:
        data = {}
        for key in sorted(self.__dict__):
            if isinstance(key_var := getattr(self, key), JsonSerializer):
                data[key] = key_var.serialize()
                continue
            data[key] = key_var
        return data

    def serialize_to_file(self, path: str = 'save.json') -> None:
        path = PathManager.get(path)
        with open(path, 'w') as f:
            f.write(json.dumps(self.serialize(), indent=2))


class JsonDeserializer:

    def deserialize(self, data: dict) -> None:
        for key in data:
            if not hasattr(self, key):
                continue
            if isinstance(key_var := getattr(self, key), JsonDeserializer):
                key_var.deserialize(data[key])
                setattr(self, key, key_var)
                continue
            setattr(self, key, data[key])

    def deserialize_from_file(self, path: str = 'save.json') -> None:
        if os.path.exists(path):
            with open(path, "r") as file:
                self.deserialize(json.load(file))


class SerDes(Singleton, JsonSerializer, JsonDeserializer):
    pass
