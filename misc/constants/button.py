import inspect
from typing import NamedTuple
import pygame as pg
from misc.constants.classes import Color


class ButtonStateColor(NamedTuple):
    text: pg.Color
    background: pg.Color


class ButtonColor(NamedTuple):
    static: ButtonStateColor
    hover: ButtonStateColor
    click: ButtonStateColor

    @staticmethod
    def get_members_list() -> list:
        members = inspect.getmembers(BUTTON_DEFAULT_COLORS, lambda member: type(member) == ButtonStateColor)
        return [item[0] for item in members]


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
