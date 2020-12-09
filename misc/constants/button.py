import inspect
from typing import NamedTuple
import pygame as pg
from misc.constants.classes import Color


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
    static=ButtonStateColor(text=Color.GRAY, background=Color.TRANSPERENT),
    hover=ButtonStateColor(text=Color.WHITE, background=Color.HALF_TRANSPERENT),
    click=ButtonStateColor(text=Color.WHITE, background=Color.JET)
)

LIGHT_BUTTON_COLORS = ButtonColor(
    static=ButtonStateColor(text=Color.SILVER, background=Color.TRANSPERENT),
    hover=ButtonStateColor(text=Color.WHITE, background=Color.HALF_TRANSPERENT),
    click=ButtonStateColor(text=Color.WHITE, background=Color.JET)
)

BUTTON_GREEN_COLORS = ButtonColor(
    static=ButtonStateColor(text=Color.SILVER, background=Color.DARK_GREEN),
    hover=ButtonStateColor(text=Color.WHITE, background=Color.GREEN),
    click=ButtonStateColor(text=Color.WHITE, background=Color.DARK_GREEN)
)

BUTTON_RED_COLORS = ButtonColor(
    static=ButtonStateColor(text=Color.SILVER, background=Color.DARK_RED),
    hover=ButtonStateColor(text=Color.WHITE, background=Color.RED),
    click=ButtonStateColor(text=Color.WHITE, background=Color.DARK_RED)
)

BUTTON_SKIN_BUY = ButtonColor(
    static=ButtonStateColor(text=Color.YELLOW, background=Color.TRANSPERENT),
    hover=ButtonStateColor(text=Color.WHITE, background=Color.HALF_TRANSPERENT),
    click=ButtonStateColor(text=Color.BLACK, background=Color.JET)
)
