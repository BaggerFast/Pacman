from pacman.data_core import EvenType, event_append
from pacman.data_core.enums import DifficultEnum

from .utils import SerDes


class SettingsStorage(SerDes):
    def __init__(self):
        self.__volume = 100
        self.DIFFICULTY = 0
        self.MUTE = False
        self.__fun = False

    # region Volume

    @property
    def volume(self) -> int:
        return self.__volume

    def set_volume(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Volume must be integer of [0, 100]")
        self.__volume = min(max(value, 0), 100)

    @property
    def fun(self) -> bool:
        return self.__fun

    def update_fun(self) -> None:
        self.__fun = not self.__fun
        event_append(EvenType.UPDATE_SOUND)

    # endregion

    # region Difficult

    def set_difficulty(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Difficult must be integer of [0, 3]")
        self.DIFFICULTY = value % len(DifficultEnum)
