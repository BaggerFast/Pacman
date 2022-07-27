from copy import deepcopy, copy

from pacman.serializers.ser import SerDes
from settings import FRUITS_COUNT
from pacman.misc.constants import SkinsNames


class SettingsSerializer(SerDes):

    def __init__(self):
        self.sound: bool = True
        self.fun: bool = False
        self.__volume: int = 100
        self.__difficulty: int = 0

    # region Getters and setter

    # region Volume

    @property
    def volume(self) -> int:
        return self.__volume

    @volume.setter
    def volume(self, value: int):
        if not isinstance(value, int):
            raise Exception('Значение уровня звук может быть только целым числом')
        self.__volume = min(max(value, 0), 100)

    # endregion

    # region Difficulty

    @property
    def difficulty(self) -> int:
        return self.__difficulty

    @difficulty.setter
    def difficulty(self, value: int):
        if not isinstance(value, int):
            raise Exception('Значение Сложности может быть только целым числом')
        self.__difficulty = value % 3

    # endregion

    # endregion


class EatenFruitsSerializer(SerDes):

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


class LevelSerializer(SerDes):

    def __init__(self):
        self.current = 0
        self.__unlocked = [[]]

    @property
    def unlocked(self):
        return deepcopy(self.__unlocked)

    def get_current_records(self, total: bool = False):
        if total:
            try:
                return self.unlocked[self.current][0] if self.unlocked[self.current][0] else 0
            except IndexError:
                return 0
        return self.unlocked[self.current]

    def update_current_records(self, score: int) -> None:
        self.unlocked[self.current].append(score)
        self.unlocked[self.current] = sorted(set(self.unlocked[self.current]), reverse=True)[:5]

    def unlock_next_level(self) -> None:
        self.unlocked.append([])

    def __str__(self):
        return f'Level: {self.current+1}'


class SkinSerializer(SerDes):

    def __init__(self):
        self.__current = SkinsNames.DEFAULT.name
        self.__unlocked = [SkinsNames.DEFAULT.name]

    def unlock_skin(self, skin: SkinsNames) -> None:
        if skin.name not in self.__unlocked and skin.name in SkinsNames.member_names_:
            self.__unlocked.append(skin.name)

    @property
    def unlocked(self) -> list:
        return copy(self.__unlocked)

    @property
    def current(self) -> str:
        return self.__current

    @current.setter
    def current(self, skin: SkinsNames):
        self.__current = skin.name if skin.name in self.__unlocked else SkinsNames.DEFAULT.name


class StorageSerializer(SerDes):

    def __init__(self) -> None:
        self.settings = SettingsSerializer()
        self.skins = SkinSerializer()
        self.levels = LevelSerializer()
        self.eaten_fruits = EatenFruitsSerializer()
