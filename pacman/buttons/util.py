from enum import auto, IntEnum

import inspect
from typing import NamedTuple
import pygame as pg
from misc.constants.classes import Color


class ButtonStateColor(NamedTuple):
    text: pg.Color = Color.WHITE
    background: pg.Color = Color.BLACK


class ButtonColor(NamedTuple):
    static: ButtonStateColor = ButtonStateColor(background=Color.RED)
    hover: ButtonStateColor = ButtonStateColor(background=Color.BLUE)
    click: ButtonStateColor = ButtonStateColor(background=Color.GREEN)

    @staticmethod
    def get_members_list() -> list:
        members = inspect.getmembers(BTN_DEFAULT_COLORS, lambda member: type(member) == ButtonStateColor)
        return [item[0] for item in members]


class BtnState(IntEnum):
    INITIAL = auto()
    HOVER = auto()
    CLICK = auto()


# region Button color presets

BTN_DEFAULT_COLORS = ButtonColor(
    static=ButtonStateColor(text=Color.GRAY, background=Color.BLACK),
    hover=ButtonStateColor(text=Color.WHITE, background=Color.JET),
    click=ButtonStateColor(text=Color.BLACK, background=Color.BLACK)
)

BTN_TRANSPERENT_COLORS = ButtonColor(
    static=ButtonStateColor(text=Color.WHITE, background=Color.TRANSPERENT),
    hover=ButtonStateColor(text=Color.WHITE, background=Color.HALF_TRANSPERENT),
    click=ButtonStateColor(text=Color.WHITE, background=Color.JET)
)

BTN_GREEN_COLORS = ButtonColor(
    static=ButtonStateColor(text=Color.WHITE, background=Color.DARK_GREEN),
    hover=ButtonStateColor(text=Color.WHITE, background=Color.GREEN),
    click=ButtonStateColor(text=Color.WHITE, background=Color.DARK_GREEN)
)

BTN_RED_COLORS = ButtonColor(
    static=ButtonStateColor(text=Color.WHITE, background=Color.DARK_RED),
    hover=ButtonStateColor(text=Color.WHITE, background=Color.RED),
    click=ButtonStateColor(text=Color.WHITE, background=Color.DARK_RED)
)

BTN_SKIN_BUY = ButtonColor(
    static=ButtonStateColor(text=Color.YELLOW, background=Color.BLACK),
    hover=ButtonStateColor(text=Color.WHITE, background=Color.JET),
    click=ButtonStateColor(text=Color.BLACK, background=Color.BLACK)
)

BTN_MENU = ButtonColor(
    static=ButtonStateColor(text=Color.GRAY, background=Color.TRANSPERENT),
    hover=ButtonStateColor(text=Color.WHITE, background=Color.TRANSPERENT),
    click=ButtonStateColor(text=Color.WHITE, background=Color.JET)
)

# endregion
