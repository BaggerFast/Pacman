from misc.patterns import Singleton
from .base import SerDes
from .settings import SettingStorage
from .fruit import FruitStorage
from .skin import SkinStorage
from .level import LevelStorage


class MainStorage(SerDes, Singleton):

    def __init__(self) -> None:
        self.setting = SettingStorage()
        self.skin = SkinStorage()
        self.level = LevelStorage()
        self.fruit = FruitStorage()
