from typing import NamedTuple

import pygame as pg

from pacman.data_core import Colors


class ButtonStateColor(NamedTuple):
    text: pg.Color = Colors.WHITE
    background: pg.Color = Colors.BLACK


class ButtonColor(NamedTuple):
    static: ButtonStateColor = ButtonStateColor(background=Colors.RED)
    hover: ButtonStateColor = ButtonStateColor(background=Colors.BLUE)
    click: ButtonStateColor = ButtonStateColor(background=Colors.GREEN)


BUTTON_DEFAULT_COLORS = ButtonColor(
    static=ButtonStateColor(text=Colors.GRAY, background=Colors.TRANSPARENT),
    hover=ButtonStateColor(text=Colors.WHITE, background=Colors.TRANSPARENT),
    click=ButtonStateColor(text=Colors.DARK_GRAY, background=Colors.HALF_TRANSPARENT),
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
