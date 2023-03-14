from typing import NamedTuple
import pygame as pg
from misc.path import get_path, get_list_path


class Sounds:
    class Tuple(NamedTuple):
        mixer: pg.mixer.Sound

    class TupleList(NamedTuple):
        list: list

    pg.mixer.init()

    CLICK = Tuple(pg.mixer.Sound(get_path("navigation", "ogg", "sounds"))).mixer
    SEED = Tuple(pg.mixer.Sound(get_path("munch", "ogg", "sounds"))).mixer
    SEED_FUN = Tuple(pg.mixer.Sound(get_path("leader", "ogg", "sounds"))).mixer
    FRUIT = Tuple(pg.mixer.Sound(get_path("eat_fruit", "ogg", "sounds"))).mixer
    GHOST = Tuple(pg.mixer.Sound(get_path("eat_ghost", "ogg", "sounds"))).mixer
    POC_INTRO = Tuple(pg.mixer.Sound(get_path("pocemon_intro", "ogg", "sounds"))).mixer
    INTERMISSION = Tuple(pg.mixer.Sound(get_path("intermission", "ogg", "sounds"))).mixer
    PELLET = Tuple(pg.mixer.Sound(get_path("power_pellet", "ogg", "sounds"))).mixer
    DEAD = TupleList(get_list_path("ogg", "sounds", "death")).list
    GAMEOVER = TupleList(get_list_path("ogg", "sounds", "gameover")).list
    INTRO = TupleList(get_list_path("ogg", "sounds", "intro")).list
    SIREN = TupleList(get_list_path("ogg", "sounds", "siren")).list


class Points:
    class Tuple(NamedTuple):
        value: int

    POINT_PER_SEED = Tuple(10).value
    POINT_PER_ENERGIZER = Tuple(50).value
    POINT_PER_FRUIT = Tuple(40).value


class Font:
    class Tuple(NamedTuple):
        size: int = 0
        font: str = ""

    TITLE = Tuple(font=get_path("title", "ttf", "fonts")).font
    DEFAULT = Tuple(font=get_path("default", "ttf", "fonts")).font
    MAIN_SCENE_SIZE = Tuple(size=10).size
    BUTTON_TEXT_SIZE = Tuple(size=24).size
    BUTTON_FOR_SKINS_TEXT_SIZE = Tuple(size=16).size
    CREDITS_SCENE_SIZE = Tuple(size=14).size
