from pygame.event import Event

from pacman.data_core import EvenType
from pacman.misc import load_sound
from pacman.skin import SkinEnum
from pacman.storage import SettingsStorage, SkinStorage

from .utils import PtxUtl


class Sounds:
    CHEAT = load_sound(PtxUtl.norm("cheat"))
    WIN = load_sound(PtxUtl.norm("lose"))
    LOSE = load_sound(PtxUtl.norm("lose"))
    CLICK = load_sound(PtxUtl.norm("click"))
    INTRO = load_sound(PtxUtl.norm("intro"))
    BACK = load_sound(PtxUtl.norm("back"))
    SEED = load_sound(PtxUtl.norm("seed"))
    DEATH = load_sound(PtxUtl.norm("death"))
    FRUIT = load_sound(PtxUtl.norm("eat_fruit"))
    GHOST = load_sound(PtxUtl.norm("eat_ghost"))
    FRIGHTENED = load_sound(PtxUtl.norm("frightened"))

    @classmethod
    def __set_default(cls):
        cls.BACK = load_sound(PtxUtl.norm("back"))
        cls.SEED = load_sound(PtxUtl.norm("seed"))
        cls.INTRO = load_sound(PtxUtl.norm("intro"))
        cls.DEATH = load_sound(PtxUtl.norm("death"))
        cls.FRUIT = load_sound(PtxUtl.norm("eat_fruit"))
        cls.GHOST = load_sound(PtxUtl.norm("eat_ghost"))
        cls.LOSE = load_sound(PtxUtl.norm("lose"))
        cls.WIN = load_sound(PtxUtl.norm("lose"))
        cls.FRIGHTENED = load_sound(PtxUtl.norm("frightened"))

    @classmethod
    def update_random_sounds(cls):
        if SettingsStorage().fun:
            cls.SEED = load_sound(PtxUtl.fun("seed"))
            cls.INTRO = load_sound(PtxUtl.fun("intro"))
            cls.DEATH = load_sound(PtxUtl.fun("death"))
            cls.LOSE = load_sound(PtxUtl.fun("lose"))
            cls.WIN = load_sound(PtxUtl.fun("win"))
        elif SkinStorage().equals(SkinEnum.STALKER):
            cls.INTRO = load_sound(PtxUtl.stalker("intro"))
            cls.DEATH = load_sound(PtxUtl.stalker("death"))
            cls.FRUIT = load_sound(PtxUtl.stalker("eat_fruit"))
            cls.GHOST = load_sound(PtxUtl.stalker("eat_ghost"))
            cls.LOSE = load_sound(PtxUtl.stalker("lose"))
            cls.WIN = load_sound(PtxUtl.stalker("win"))

    @classmethod
    def __reload_sound(cls):
        cls.__set_default()
        cls.update_random_sounds()
        if SettingsStorage().fun:
            return
        if SkinStorage().equals(SkinEnum.POKEBALL):
            cls.INTRO = load_sound("pokeball/intro")
        elif SkinStorage().equals(SkinEnum.VALVE):
            cls.BACK = load_sound(PtxUtl.valve("back"))
            cls.SEED = load_sound(PtxUtl.valve("seed"))
            cls.INTRO = load_sound(PtxUtl.valve("intro"))
            cls.DEATH = load_sound(PtxUtl.valve("death"))
            cls.FRUIT = load_sound(PtxUtl.valve("eat_fruit"))
            cls.GHOST = load_sound(PtxUtl.valve("eat_ghost"))
            cls.FRIGHTENED = load_sound(PtxUtl.valve("frightened"))
        elif SkinStorage().equals(SkinEnum.WINDOWS):
            cls.SEED = load_sound(PtxUtl.win("seed"))
            cls.INTRO = load_sound(PtxUtl.win("intro"))
            cls.DEATH = load_sound(PtxUtl.win("death"))
            cls.FRUIT = load_sound(PtxUtl.win("eat_fruit"))
            cls.GHOST = load_sound(PtxUtl.win("eat_ghost"))

    @classmethod
    def event_handler(cls, event: Event):
        if event.type == EvenType.UPDATE_SOUND:
            cls.__reload_sound()
