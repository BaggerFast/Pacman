from misc.patterns import Singleton
from misc.skins import SkinNames
from misc.storage.base import SerDes


class SkinStorage(SerDes, Singleton):

    def __init__(self):
        self.__current = SkinNames.DEFAULT.name
        self.__unlocked = [SkinNames.DEFAULT.name]

    def unlock_skin(self, skins: SkinNames) -> None:
        if isinstance(skins, SkinNames):
            raise Exception
        if skins.name not in self.__unlocked and skins.name in SkinNames.member_names_:
            self.__unlocked.append(skins.name)

    def is_unlock(self, skin: SkinNames) -> bool:
        return skin.name in self.__unlocked

    @property
    def current(self) -> str:
        return self.__current

    @current.setter
    def current(self, skins: SkinNames):
        if skins.name not in self.__unlocked:
            raise Exception
        self.__current = skins.name
