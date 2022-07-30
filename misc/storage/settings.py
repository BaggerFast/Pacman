from misc.patterns import Singleton
from misc.storage.base import SerDes


class SettingStorage(SerDes, Singleton):

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

    def swap_sound(self):
        self.sound = not self.sound

    def swap_fun(self):
        self.fun = not self.fun

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
