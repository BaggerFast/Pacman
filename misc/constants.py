import inspect
import os.path
from typing import NamedTuple, List, Union
import pygame as pg
from misc.path import get_sound_path


class Sounds:
    class Tuple(NamedTuple):
        value: str
    pg.mixer.init()
    CLICK = pg.mixer.Sound(get_sound_path(Tuple("NAV").value))
    DEAD = pg.mixer.Sound(get_sound_path(Tuple("pacman_death").value))
    GAMEOVER = pg.mixer.Sound(get_sound_path(Tuple("GameOver").value))
    BOOST = pg.mixer.Sound(get_sound_path(Tuple("pacman_intermission").value))
    SEED = pg.mixer.Sound(get_sound_path(Tuple("leader2").value))
    INTRO = pg.mixer.Sound(get_sound_path(Tuple("pacman_beginning").value))
    MOVE = pg.mixer.Sound(get_sound_path(Tuple("pacman_chomp").value))
    # GAMESTART = pg.mixer.Sound(get_sound_path(Mixer("Star").value))


class Color(NamedTuple):
    class Tuple(NamedTuple):
        color: pg.Color
    RED = Tuple(pg.Color('red')).color
    BLUE = Tuple(pg.Color('blue')).color
    GREEN = Tuple(pg.Color('green')).color
    BLACK = Tuple(pg.Color('black')).color
    WHITE = Tuple(pg.Color('white')).color
    ORANGE = Tuple(pg.Color('orange')).color
    YELLOW = Tuple(pg.Color('yellow')).color
    GOLD = Tuple(pg.Color('gold')).color
    GRAY = Tuple(pg.Color('gray50')).color
    DARK_GRAY = Tuple(pg.Color('gray26')).color
    SILVER = Tuple(pg.Color(192, 192, 192)).color
    BRONZE = Tuple(pg.Color(205, 127, 50)).color
    WOODEN = Tuple(pg.Color(101, 67, 33)).color
    JET = Tuple(pg.Color(10, 10, 10)).color


class ButtonStateColor(NamedTuple):
    text: pg.Color = Color.WHITE
    background: pg.Color = Color.BLACK

    @staticmethod
    def get_members_list() -> list:
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
    def get_members_list() -> list:
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


class Points:
    class Tuple(NamedTuple):
        value: int
    POINT_PER_SEED = Tuple(10).value
    POINT_PER_ENERGIZER = Tuple(50).value
    POINT_PER_FRUIT = Tuple(40).value


class Font:
    class Tuple(NamedTuple):
        size: int = 0
        font: str = ''
    TITLE = Tuple(font=os.path.join(ROOT_DIR, 'fonts', 'title.ttf')).font
    DEFAULT = Tuple(font=os.path.join(ROOT_DIR, 'fonts', 'default.ttf')).font
    MAIN_SCENE_SIZE = Tuple(size=10).size
    BUTTON_TEXT_SIZE = Tuple(size=24).size
    CREDITS_SCENE_SIZE = Tuple(size=14).size


class Maps(NamedTuple):
    class Tuple(NamedTuple):
        value: Union[str, int]
    level_1 = Tuple("original.json").value
    level_2 = Tuple("new_map.json").value
    level_3 = Tuple("new_new_map.json").value
    MAPS_COUNT = Tuple(3).value

    @staticmethod
    def get(attr: str) -> str:
        return getattr(Maps, attr)

    @staticmethod
    def keys() -> List[str]:
        return [f"level_{index}" for index in range(Maps.MAPS_COUNT)]


DUBUG = True
