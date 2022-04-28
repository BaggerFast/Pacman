from meta_classes import Singleton
from misc.constants import FRUITS_COUNT, SkinsNames


class BaseSerializer(Singleton):

    # region Public

    def serialize_to_dict(self) -> dict:
        data = {}
        for key in sorted(self.__dict__):
            key_var = getattr(self, key)
            if isinstance(key_var, BaseSerializer):
                data[key] = key_var.serialize_to_dict()
                continue
            data[key] = key_var
        return data

    def deserialize_from_dict(self, value: dict):
        for key in value:
            if not hasattr(self, key):
                continue
            key_var = getattr(self, key)
            if isinstance(key_var, BaseSerializer):
                key_var.deserialize_from_dict(value[key])
                setattr(self, key, key_var)
                continue
            setattr(self, key, value[key])

    # endregion


class SettingsSerializer(BaseSerializer):

    def __init__(self):
        self.SOUND = True
        self.FUN = False
        self.VOLUME = 100
        self.DIFFICULTY = 0

    def change_volume(self, num: int):
        self.VOLUME = min(max(self.VOLUME + num, 0), 100)

    def change_difficulty(self):
        self.DIFFICULTY = (self.DIFFICULTY+1) % 3


class EatenFruitsSerializer(BaseSerializer):

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


class SkinSerializer(BaseSerializer):

    def __init__(self):
        self.current = SkinsNames.default
        self.unlocked = [SkinsNames.default]


class LevelSerializer(BaseSerializer):

    def __init__(self):
        self.current = 0
        self.unlocked = [[]]

    def get_current_records(self, total: bool = False) -> list[int]:
        if total:
            return self.unlocked[self.current][0] if self.unlocked[self.current][0] else 0
        return self.unlocked[self.current]

    def update_current_records(self, score: int) -> None:
        self.unlocked[self.current].append(score)
        self.unlocked[self.current] = sorted(set(self.unlocked[self.current]), reverse=True)[:5]


class StorageSerializer(BaseSerializer):

    def __init__(self, game) -> None:
        self.settings = SettingsSerializer()
        self.skins = SkinSerializer()
        self.levels = LevelSerializer()
        self.eaten_fruits = EatenFruitsSerializer()
