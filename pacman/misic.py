from abc import ABC
from random import choice

from pygame.event import Event

from pacman.data_core import Dirs, PathUtil
from pacman.events.events import EvenType
from pacman.misc.serializers import SettingsStorage, SkinStorage
from pacman.misc.singleton import Singleton
from pacman.misc.sound_controller import SoundController
from pacman.misc.tmp_skin import SkinEnum


class PtxUtl(ABC):
    @staticmethod
    def norm(path: str) -> str:
        return f"default/{path}"

    @staticmethod
    def fun(path: str) -> str:
        return choice(PathUtil.get_list(f"{Dirs.SOUND}/fun/{path}"))

    @staticmethod
    def valve(path: str) -> str:
        return f"valve/{path}"

    @staticmethod
    def win(path: str) -> str:
        return f"windows/{path}"


class Music(Singleton):
    def __init__(self):
        self.CLICK = SoundController(PtxUtl.norm("click"))
        self.BACK = SoundController(PtxUtl.norm("back"), 3)
        self.SEED = SoundController(PtxUtl.norm("seed"), 4)
        self.INTRO = SoundController(PtxUtl.norm("intro"))
        self.DEATH = SoundController(PtxUtl.norm("death"))
        self.FRUIT = SoundController(PtxUtl.norm("eat_fruit"), 4)
        self.GHOST = SoundController(PtxUtl.norm("eat_ghost"), 4)
        self.LOSE = SoundController(PtxUtl.norm("lose"), 2)
        self.FRIGHTENED = SoundController(PtxUtl.norm("frightened"), 6)

        self.__reload_sound(False)

    def __set_default(self):
        self.BACK.set_sound(PtxUtl.norm("back"))
        self.SEED.set_sound(PtxUtl.norm("seed"))
        self.INTRO.set_sound(PtxUtl.norm("intro"))
        self.DEATH.set_sound(PtxUtl.norm("death"))
        self.FRUIT.set_sound(PtxUtl.norm("eat_fruit"))
        self.GHOST.set_sound(PtxUtl.norm("eat_ghost"))
        self.LOSE.set_sound(PtxUtl.norm("lose"))
        self.FRIGHTENED.set_sound(PtxUtl.norm("frightened"))

    def update_fun(self):
        if SettingsStorage().fun:
            self.SEED.set_sound(PtxUtl.fun("seed"))
            self.INTRO.set_sound(PtxUtl.fun("intro"))
            self.DEATH.set_sound(PtxUtl.fun("death"))
            self.LOSE.set_sound(PtxUtl.fun("lose"))

    def __reload_sound(self, with_default: bool = True):
        if with_default:
            self.__set_default()
        if SettingsStorage().fun:
            self.update_fun()
        elif SkinStorage().equals(SkinEnum.POKEBALL):
            self.INTRO.set_sound("pokeball/intro")
        elif SkinStorage().equals(SkinEnum.VALVE):
            self.BACK.set_sound(PtxUtl.valve("back"))
            self.SEED.set_sound(PtxUtl.valve("seed"))
            self.INTRO.set_sound(PtxUtl.valve("intro"))
            self.DEATH.set_sound(PtxUtl.valve("death"))
            self.FRUIT.set_sound(PtxUtl.valve("eat_fruit"))
            self.GHOST.set_sound(PtxUtl.valve("eat_ghost"))
            self.FRIGHTENED.set_sound(PtxUtl.valve("frightened"))
        elif SkinStorage().equals(SkinEnum.WINDOWS):
            self.SEED.set_sound(PtxUtl.win("seed"))
            self.INTRO.set_sound(PtxUtl.win("intro"))
            self.DEATH.set_sound(PtxUtl.win("death"))
            self.FRUIT.set_sound(PtxUtl.win("eat_fruit"))
            self.GHOST.set_sound(PtxUtl.win("eat_ghost"))

    def event_handler(self, event: Event):
        if event.type == EvenType.UPDATE_SOUND:
            self.__reload_sound()
