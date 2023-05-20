from pacman.misc.singleton import Singleton


class JsonSerializer:
    def serialize(self) -> dict:
        data = {}
        for key in sorted(self.__dict__):
            key_var = getattr(self, key)
            if isinstance(key_var, JsonSerializer):
                data[key] = key_var.serialize()
                continue
            data[key] = key_var
        return data


class JsonDeserializer:
    def deserialize(self, value: dict) -> None:
        for key in value:
            if not hasattr(self, key):
                continue
            key_var = getattr(self, key)
            if not isinstance(key_var, JsonDeserializer):
                setattr(self, key, value[key])
                continue
            key_var.deserialize(value[key])
            setattr(self, key, key_var)
            continue


class SerDes(Singleton, JsonSerializer, JsonDeserializer):
    pass
