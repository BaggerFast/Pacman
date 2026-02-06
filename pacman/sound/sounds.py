from pygame.event import Event

from pacman.data_core import EvenType
from pacman.misc import load_sound
from pacman.skin import SkinEnum
from pacman.storage import SettingsStorage, SkinStorage

from .utils import SoundUtil


class Sounds:
    CHEAT = load_sound(SoundUtil.norm("cheat"))
    WIN = load_sound(SoundUtil.norm("lose"))
    LOSE = load_sound(SoundUtil.norm("lose"))
    CLICK = load_sound(SoundUtil.norm("click"))
    INTRO = load_sound(SoundUtil.norm("intro"))
    BACK = load_sound(SoundUtil.norm("back"))
    SEED = load_sound(SoundUtil.norm("seed"))
    DEATH = load_sound(SoundUtil.norm("death"))
    FRUIT = load_sound(SoundUtil.norm("eat_fruit"))
    GHOST = load_sound(SoundUtil.norm("eat_ghost"))
    FRIGHTENED = load_sound(SoundUtil.norm("frightened"))

    @classmethod
    def __set_default(cls):
        cls.BACK = load_sound(SoundUtil.norm("back"))
        cls.SEED = load_sound(SoundUtil.norm("seed"))
        cls.INTRO = load_sound(SoundUtil.norm("intro"))
        cls.DEATH = load_sound(SoundUtil.norm("death"))
        cls.FRUIT = load_sound(SoundUtil.norm("eat_fruit"))
        cls.GHOST = load_sound(SoundUtil.norm("eat_ghost"))
        cls.LOSE = load_sound(SoundUtil.norm("lose"))
        cls.WIN = load_sound(SoundUtil.norm("lose"))
        cls.FRIGHTENED = load_sound(SoundUtil.norm("frightened"))

    @classmethod
    def update_random_sounds(cls):
        if SettingsStorage().fun:
            cls.SEED = load_sound(SoundUtil.fun("seed"))
            cls.INTRO = load_sound(SoundUtil.fun("intro"))
            cls.DEATH = load_sound(SoundUtil.fun("death"))
            cls.LOSE = load_sound(SoundUtil.fun("lose"))
            cls.WIN = load_sound(SoundUtil.fun("win"))
        elif SkinStorage().equals(SkinEnum.STALKER):
            cls.INTRO = load_sound(SoundUtil.stalker("intro"))
            cls.DEATH = load_sound(SoundUtil.stalker("death"))
            cls.FRUIT = load_sound(SoundUtil.stalker("eat_fruit"))
            cls.GHOST = load_sound(SoundUtil.stalker("eat_ghost"))
            cls.LOSE = load_sound(SoundUtil.stalker("lose"))
            cls.WIN = load_sound(SoundUtil.stalker("win"))

    @classmethod
    def __reload_sound(cls):
        cls.__set_default()
        cls.update_random_sounds()
        if SettingsStorage().fun:
            return
        if SkinStorage().equals(SkinEnum.POKEBALL):
            cls.INTRO = load_sound("pokeball/intro")
        elif SkinStorage().equals(SkinEnum.VALVE):
            cls.BACK = load_sound(SoundUtil.valve("back"))
            cls.SEED = load_sound(SoundUtil.valve("seed"))
            cls.INTRO = load_sound(SoundUtil.valve("intro"))
            cls.DEATH = load_sound(SoundUtil.valve("death"))
            cls.FRUIT = load_sound(SoundUtil.valve("eat_fruit"))
            cls.GHOST = load_sound(SoundUtil.valve("eat_ghost"))
            cls.FRIGHTENED = load_sound(SoundUtil.valve("frightened"))
        elif SkinStorage().equals(SkinEnum.WINDOWS):
            cls.SEED = load_sound(SoundUtil.win("seed"))
            cls.INTRO = load_sound(SoundUtil.win("intro"))
            cls.DEATH = load_sound(SoundUtil.win("death"))
            cls.FRUIT = load_sound(SoundUtil.win("eat_fruit"))
            cls.GHOST = load_sound(SoundUtil.win("eat_ghost"))

    @classmethod
    def event_handler(cls, event: Event):
        if event.type == EvenType.UPDATE_SOUND:
            cls.__reload_sound()
