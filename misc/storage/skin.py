from misc.patterns import Singleton
from misc.storage.base import SerDes


class SkinStorage(SerDes, Singleton):

    # def __init__(self):
    #     self.__current = SkinsNames.DEFAULT.name
    #     self.__unlocked = [SkinsNames.DEFAULT.name]
    #
    # def unlock_skin(self, skins: SkinsNames) -> None:
    #     if skins.name not in self.__unlocked and skins.name in SkinsNames.member_names_:
    #         self.__unlocked.append(skins.name)
    #
    # @property
    # def unlocked(self) -> list:
    #     return copy(self.__unlocked)

    @property
    def current(self) -> str:
        return self.__current
    #
    # @current.setter
    # def current(self, skins: SkinsNames):
    #     self.__current = skins.name if skins.name in self.__unlocked else SkinsNames.DEFAULT.name
