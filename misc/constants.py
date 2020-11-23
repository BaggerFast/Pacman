import inspect
import os.path
from typing import NamedTuple

import pygame as pg


# https://www.pygame.org/docs/ref/color.html
# https://github.com/pygame/pygame/blob/master/src_py/colordict.py
class Color:
    RED = pg.color.Color('red')
    BLUE = pg.color.Color('blue')
    GREEN = pg.color.Color('green')
    BLACK = pg.color.Color('black')
    WHITE = pg.color.Color('white')
    ORANGE = pg.color.Color('orange')
    YELLOW = pg.color.Color('yellow')
    GOLD = pg.color.Color('gold')
    GRAY = pg.color.Color('gray50')
    DARK_GRAY = pg.color.Color('gray26')
    SILVER = pg.color.Color(192, 192, 192)
    BRONZE = pg.color.Color(205, 127, 50)
    WOODEN = pg.color.Color(101, 67, 33)


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
        section = self.__getattribute__(name)
        default_section = BUTTON_DEFAULT_COLORS.__getattribute__(name)

        if name in data.keys():
            for item in [ButtonStateColor.get_members_list()]:
                if item in data[name].keys():
                    section.__setattr__(item,data[name][item])
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
    hover=ButtonStateColor(text=Color.WHITE, background=(10, 10, 10)),
    click=ButtonStateColor(text=Color.BLACK, background=Color.BLACK)
)


ROOT_DIR = os.path.dirname(os.path.abspath('run.py'))
CELL_SIZE = 8


class Points:
    POINT_PER_SEED = 10
    POINT_PER_ENERGIZER = 50


class Font:
    FILENAME = os.path.join(ROOT_DIR, 'fonts', 'font0.ttf')
    ALTFONT = os.path.join(ROOT_DIR, 'fonts', 'font1.ttf')
    MAIN_SCENE_SIZE = 10
    BUTTON_TEXT_SIZE = 24
    TITERS_SCENE_SIZE = 14


MAPS = {
    "level_1": "original.json",
    "level_2": "new_map.json"
}

MAPS_COUNT = len(MAPS)
