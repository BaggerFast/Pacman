from misc.constants import FRUITS_COUNT


class SerializerField:

    # region Public

    def serialize_to_dict(self) -> dict:
        data = {}
        for key in sorted(self.__dict__):
            key_var = getattr(self, key)
            if isinstance(key_var, SerializerField):
                data[key] = key_var.serialize_to_dict()
                continue
            data[key] = key_var
        print(self.__dict__)
        return data

    def deserialize_from_dict(self, value: dict):
        for key in value:
            key_var = getattr(self, key)
            if isinstance(key_var, SerializerField):
                key_var.deserialize_from_dict(value[key])
                setattr(self, key, key_var)
                continue
            setattr(self, key, value[key])

    # endregion


class SettingsSerializer(SerializerField):

    def __init__(self):
        self.SOUND = True
        self.FUN = False
        self.VOLUME = 100
        self.DIFFICULTY = 0


class EatenFruitsSerializer(SerializerField):

    def __init__(self):
        self.__fruits = []

    def __getitem__(self, item: int) -> int:
        try:
            return self.__fruits[item]
        except IndexError:
            return 0

    def __setitem__(self, key: int, value: int) -> None:
        if key in range(FRUITS_COUNT):
            if isinstance(value, int):
                try:
                    self.__fruits[key] = value
                except IndexError:
                    self.__fruits.append(value)
            else:
                raise Exception(f"Fruit value must be int type, instead of {type(value)}")
        else:
            raise Exception(f"Id error. FruitController id: {key} doesn't exist")

    def __len__(self):
        return len(self.__fruits)

    def __str__(self):
        print(self.__fruits)
