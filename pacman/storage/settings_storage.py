from .utils import SerDes


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
