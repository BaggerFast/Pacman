import json
from json import JSONDecodeError
from pacman.misc.singleton import Singleton
from pacman.misc.skins import Skin
from pacman.misc.tmp_skin import SkinEnum


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
        self.__unlocked = [SkinEnum.DEFAULT.name]
        self.__current = SkinEnum.DEFAULT.name

    def unlock_skin(self, skin: SkinEnum) -> None:
        skin_name = skin.name
        if not self.is_unlocked(skin):
            self.__unlocked.append(skin_name)
            self.__current = skin.name

    def is_unlocked(self, skin: SkinEnum) -> bool:
        return skin.name in self.__unlocked

    @property
    def current(self) -> SkinEnum:
        try:
            return SkinEnum[self.__current]
        except KeyError:
            raise Exception("Invalid skin")

    @property
    def current_instance(self) -> Skin:
        try:
            return SkinEnum[self.__current].value
        except KeyError:
            raise Exception("Invalid skin")

    def equals(self, skin: SkinEnum) -> bool:
        return self.__current is skin

    def set_skin(self, skin: SkinEnum):
        if self.is_unlocked(skin):
            self.__current = skin.name
        else:
            raise Exception("Invalid skin")


class LevelStorage(SerDes):
    def __init__(self):
        self.level_count = 10
        self.unlocked = []
        self.__current = 0

    @property
    def current(self) -> int:
        return self.__current

    @current.setter
    def current(self, value):
        if isinstance(value, int) and 0 <= value < self.level_count:
            self.__current = value % len(self.unlocked)
        else:
            raise Exception(f"Current level must be in 0 <= {value} < {self.level_count}")

    def unlock_next_level(self) -> None:
        if len(self.unlocked) < self.level_count:
            self.unlocked.append([0])

    def set_next_level(self):
        self.current = self.current + 1

    def set_prev_level(self):
        self.current = self.current - 1

    def current_highscores(self):
        if self.__current > len(self.unlocked) - 1:
            return []
        self.unlocked[self.__current] = sorted(self.unlocked[self.__current], reverse=True)[0:5]
        return self.unlocked[self.__current]

    def get_highscore(self) -> int:
        if self.__current > len(self.unlocked) - 1:
            return 0
        highscore = self.current_highscores()
        if not highscore:
            return 0
        return highscore[0]

    def add_record(self, score: int):
        if self.__current > len(self.unlocked) - 1:
            return
        self.unlocked[self.__current].append(int(score))
        self.unlocked = self.current_highscores()

    def is_last_level(self) -> bool:
        return LevelStorage().current + 1 >= self.level_count

    def __str__(self):
        return f"Level {self.current + 1}"


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


class FruitStorage(SerDes):

    def __init__(self):
        self.__fruit_count = 7
        self.eaten_fruits = [0 for _ in range(self.__fruit_count)]

    def store_fruit(self, fruit_id: int = 0, value: int = 0) -> None:
        if fruit_id in range(7):
            self.eaten_fruits[fruit_id] += value
        else:
            raise Exception(f"id error. Fruit id: {fruit_id} doesn't exist")

    # endregion


class MainStorage(SerDes):
    def __init__(self):
        self.__settings = SettingsStorage()
        self.__skins = SkinStorage()
        self.__levels = LevelStorage()
        self.__fruit = FruitStorage()


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
