from .fruit_storage import FruitStorage
from .level_storage import LevelStorage
from .settings_storage import SettingsStorage
from .skin_storage import SkinStorage
from .utils import SerDes


class MainStorage(SerDes):
    def __init__(self):
        self.__settings = SettingsStorage()
        self.__skins = SkinStorage()
        self.__levels = LevelStorage()
        self.__fruit = FruitStorage()
