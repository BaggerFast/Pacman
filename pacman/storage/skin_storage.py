from pygame.event import Event

from pacman.data_core import EvenType, event_append
from pacman.skin import Skin, SkinEnum

from .utils import SerDes


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
        return self.current is skin

    def set_skin(self, skin: SkinEnum):
        if self.is_unlocked(skin):
            self.__current = skin.name
            event_append(EvenType.UPDATE_SOUND)
        else:
            raise Exception("Invalid skin")

    def event_handler(self, event: Event) -> None:
        if event.type == EvenType.UNLOCK_SAVES:
            self.__unlocked = []
            for skin in SkinEnum:
                self.__unlocked.append(skin.name)
