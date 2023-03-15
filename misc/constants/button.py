import inspect
from typing import NamedTuple
import pygame as pg

from data_core import Colors


class ButtonStateColor(NamedTuple):
    text: pg.Color = Colors.WHITE
    background: pg.Color = Colors.BLACK

    @staticmethod
    def get_members_list() -> list:
        members = inspect.getmembers(BUTTON_DEFAULT_COLORS, lambda member: isinstance(member, pg.Color))
        return [item[0] for item in members]


class ButtonColor(NamedTuple):
    static: ButtonStateColor = ButtonStateColor(background=Colors.RED)
    hover: ButtonStateColor = ButtonStateColor(background=Colors.BLUE)
    click: ButtonStateColor = ButtonStateColor(background=Colors.GREEN)

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
    static=ButtonStateColor(text=Colors.GRAY, background=Colors.BLACK),
    hover=ButtonStateColor(text=Colors.WHITE, background=Colors.JET),
    click=ButtonStateColor(text=Colors.BLACK, background=Colors.BLACK),
)

BUTTON_TRANSPERENT_COLORS = ButtonColor(
    static=ButtonStateColor(text=Colors.GRAY, background=Colors.TRANSPARENT),
    hover=ButtonStateColor(text=Colors.WHITE, background=Colors.HALF_TRANSPARENT),
    click=ButtonStateColor(text=Colors.WHITE, background=Colors.JET),
)

BUTTON_GREEN_COLORS = ButtonColor(
    static=ButtonStateColor(text=Colors.WHITE, background=Colors.DARK_GREEN),
    hover=ButtonStateColor(text=Colors.WHITE, background=Colors.GREEN),
    click=ButtonStateColor(text=Colors.WHITE, background=Colors.DARK_GREEN),
)

BUTTON_RED_COLORS = ButtonColor(
    static=ButtonStateColor(text=Colors.WHITE, background=Colors.DARK_RED),
    hover=ButtonStateColor(text=Colors.WHITE, background=Colors.RED),
    click=ButtonStateColor(text=Colors.WHITE, background=Colors.DARK_RED),
)

BUTTON_SKIN_BUY = ButtonColor(
    static=ButtonStateColor(text=Colors.YELLOW, background=Colors.BLACK),
    hover=ButtonStateColor(text=Colors.WHITE, background=Colors.JET),
    click=ButtonStateColor(text=Colors.BLACK, background=Colors.BLACK),
)

BUTTON_MENU = ButtonColor(
    static=ButtonStateColor(text=Colors.GRAY, background=Colors.TRANSPARENT),
    hover=ButtonStateColor(text=Colors.WHITE, background=Colors.TRANSPARENT),
    click=ButtonStateColor(text=Colors.WHITE, background=Colors.JET),
)
