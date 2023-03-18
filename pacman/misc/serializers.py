import json
from json import JSONDecodeError

from pacman.misc import FRUITS_COUNT, HIGHSCORES_COUNT
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


class SkinStorage(SerDes):
    def __init__(self):
        self.unlocked = ["default"]
        self.current = "default"

    def unlock_skin(self, skin_name: str = 0) -> None:
        if skin_name not in MainStorage().skins.unlocked:
            self.unlocked.append(skin_name)
        else:
            raise Exception(f"Name error. Skin name: {skin_name} doesn't exist")


class LevelStorage(SerDes):
    def __init__(self):
        self.current = 0
        self.unlocked = [0]

    def unlock_level(self, level_id: int = 0) -> None:
        if level_id not in MainStorage().levels.unlocked:
            self.unlocked.append(level_id)


class SettingsStorage(SerDes):
    def __init__(self):
        self.volume = 100
        self.difficulty = 0
        self.mute = False
        self.fun = False

    # region Volume

    def set_volume(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Volume must be integer of [0, 100]")
        self.volume = min(max(value, 0), 100)

    # endregion

    # region Difficult

    def set_difficulty(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Difficult must be integer of [0, 3]")
        self.difficulty = value % 3

    # endregion


class MainStorage(SerDes):
    def __init__(self):
        self.settings = SettingsStorage()
        self.skins = SkinStorage()
        self.levels = LevelStorage()
        self.eaten_fruits = [0 for _ in range(FRUITS_COUNT)]
        self.highscores = [[0 for _ in range(HIGHSCORES_COUNT)] for _ in range(10)]

    def store_fruit(self, fruit_id: int = 0, value: int = 0) -> None:
        if fruit_id in range(FRUITS_COUNT):
            self.eaten_fruits[fruit_id] += value
        else:
            raise Exception(f"id error. Fruit id: {fruit_id} doesn't exist")


class StorageLoader:
    def __init__(self, path: str):
        self.__path = path

    def to_file(self) -> None:
        string = json.dumps(MainStorage().serialize(), indent=2)
        with open(self.__path, "w") as f:
            f.write(string)

    def from_file(self) -> None:
        try:
            with open(self.__path, "r") as f:
                MainStorage().deserialize(json.load(f))
        except (FileNotFoundError, JSONDecodeError):
            self.to_file()
