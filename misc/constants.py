import inspect
import os.path
from typing import NamedTuple
import pygame as pg
from misc.path import get_sound_path


class Palitra(NamedTuple):
    color: pg.color.Color

class Mixer(NamedTuple):
    value: str

SOUNDS = []


class Sounds:
    # CLICK = Mixer("NAV").value
    pg.mixer.init()
    CLICK = pg.mixer.Sound(get_sound_path(Mixer("NAV").value))
    DEAD = pg.mixer.Sound(get_sound_path(Mixer("pacman_death").value))
    GAMEOVER = pg.mixer.Sound(get_sound_path(Mixer("GameOver").value))
    BOOST = pg.mixer.Sound(get_sound_path(Mixer("pacman_intermission").value))
    SEED = pg.mixer.Sound(get_sound_path(Mixer("leader2").value))
    INTRO = pg.mixer.Sound(get_sound_path(Mixer("pacman_beginning").value))
    MOVE = pg.mixer.Sound(get_sound_path(Mixer("pacman_chomp").value))
    # GAMESTART = pg.mixer.Sound(get_sound_path(Mixer("Star").value))


class Color:
    RED = Palitra(pg.color.Color('red')).color
    BLUE = Palitra(pg.color.Color('blue')).color
    GREEN = Palitra(pg.color.Color('green')).color
    BLACK = Palitra(pg.color.Color('black')).color
    WHITE = Palitra(pg.color.Color('white')).color
    ORANGE = Palitra(pg.color.Color('orange')).color
    YELLOW = Palitra(pg.color.Color('yellow')).color
    GOLD = Palitra(pg.color.Color('gold')).color
    GRAY = Palitra(pg.color.Color('gray50')).color
    DARK_GRAY = Palitra(pg.color.Color('gray26')).color
    SILVER = Palitra(pg.color.Color(192, 192, 192)).color
    BRONZE = Palitra(pg.color.Color(205, 127, 50)).color
    WOODEN = Palitra(pg.color.Color(101, 67, 33)).color
    JET = Palitra(pg.color.Color(10, 10, 10)).color


class ButtonStateColor(NamedTuple):
    text: pg.Color = Color.WHITE
    background: pg.Color = Color.BLACK

    @staticmethod
    def get_members_list():
        members = inspect.getmembers(BUTTON_DEFAULT_COLORS, lambda member: type(member) == pg.Color)
        return [item[0] for item in members]


class ButtonColor(NamedTuple):
    static: ButtonStateColor = ButtonStateColor(background=Color.RED)
    hover: ButtonStateColor = ButtonStateColor(background=Color.BLUE)
    click: ButtonStateColor = ButtonStateColor(background=Color.GREEN)

    def init_section(self, name: str, data: dict) -> None:
        section = self.__getattribute__(name)
        default_section = BUTTON_DEFAULT_COLORS.__getattribute__(name)
        """
                                     ▄              ▄
                                    ▌▒█           ▄▀▒▌
                                    ▌▒▒█        ▄▀▒▒▒▐
                                   ▐▄█▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐
                                 ▄▄▀▒▒▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐
        METAPROGRAMMING IS     ▄▀▒▒▒░░░▒▒▒░░░▒▒▒▀██▀▒▌
        A SUCH WOW THING =)   ▐▒▒▒▄▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄▒▌
                              ▌░░▌█▀▒▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐
                             ▐░░░▒▒▒▒▒▒▒▒▌██▀▒▒░░░▒▒▒▀▄▌
                             ▌░▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░▒▒▒▒▌
                            ▌▒▒▒▄██▄▒▒▒▒▒▒▒▒░░░░░░░░▒▒▒▐
                            ▐▒▒▐▄█▄█▌▒▒▒▒▒▒▒▒▒▒░▒░▒░▒▒▒▒▌
                            ▐▒▒▐▀▐▀▒▒▒▒▒▒▒▒▒▒▒▒▒░▒░▒░▒▒▐
                             ▌▒▒▀▄▄▄▄▄▄▀▒▒▒▒▒▒▒░▒░▒░▒▒▒▌
                             ▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒░▒▒▄▒▒▐
                              ▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒░▒░▒▄▒▒▒▒▌
                                ▀▄▒▒▒▒▒▒▒▒▒▒▄▄▄▀▒▒▒▒▄▀
                                  ▀▄▄▄▄▄▄▀▀▀▒▒▒▒▒▄▄▀
                                     ▀▀▀▀▀▀▀▀▀▀▀▀
        """
        if name in data.keys():
            for item in [ButtonStateColor.get_members_list()]:
                if item in data[name].keys():
                    section.__setattr__(item, data[name][item])
        else:
            self.__setattr__(name, default_section)

    @staticmethod
    def get_members_list():
        members = inspect.getmembers(BUTTON_DEFAULT_COLORS, lambda member: type(member) == ButtonStateColor)
        return [item[0] for item in members]

    def from_dict(self, data: dict) -> None:
        member_names = self.get_members_list()
        for name in member_names:
            self.init_section(name, data)


BUTTON_DEFAULT_COLORS = ButtonColor(
    static=ButtonStateColor(text=Color.GRAY, background=Color.BLACK),
    hover=ButtonStateColor(text=Color.WHITE, background=Color.JET),
    click=ButtonStateColor(text=Color.BLACK, background=Color.BLACK)
)

ROOT_DIR = os.path.dirname(os.path.abspath('run.py'))
CELL_SIZE = 8


# TODO: migrate to NamedTuple
class Points:
    POINT_PER_SEED = 10
    POINT_PER_ENERGIZER = 50


# TODO: migrate to NamedTuple
class Font:
    FILENAME = os.path.join(ROOT_DIR, 'fonts', 'font0.ttf')
    ALTFONT = os.path.join(ROOT_DIR, 'fonts', 'font1.ttf')
    MAIN_SCENE_SIZE = 10
    BUTTON_TEXT_SIZE = 24
    CREDITS_SCENE_SIZE = 14


MAPS = {
    "level_1": "original.json",
    "level_2": "new_map.json"
}

MAPS_COUNT = len(MAPS)
