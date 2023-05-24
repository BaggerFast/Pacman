from typing import NamedTuple

from pygame import Color

from pacman.data_core import Colors


class BtnStateColor(NamedTuple):
    text: Color = Colors.WHITE
    background: Color = Colors.BLACK


class BtnColor(NamedTuple):
    static: BtnStateColor
    hover: BtnStateColor
    click: BtnStateColor


BTN_DEF_COLORS = BtnColor(
    static=BtnStateColor(text=Colors.GRAY, background=Colors.TRANSPARENT),
    hover=BtnStateColor(text=Colors.WHITE, background=Colors.TRANSPARENT),
    click=BtnStateColor(text=Colors.DARK_GRAY, background=Colors.HALF_TRANSPARENT),
)

BTN_GREEN_COLORS = BtnColor(
    static=BtnStateColor(text=Colors.WHITE, background=Colors.DARK_GREEN),
    hover=BtnStateColor(text=Colors.WHITE, background=Colors.GREEN),
    click=BtnStateColor(text=Colors.WHITE, background=Colors.DARK_GREEN),
)

BTN_RED_COLORS = BtnColor(
    static=BtnStateColor(text=Colors.WHITE, background=Colors.DARK_RED),
    hover=BtnStateColor(text=Colors.WHITE, background=Colors.RED),
    click=BtnStateColor(text=Colors.WHITE, background=Colors.DARK_RED),
)

BTN_SKIN_BUY = BtnColor(
    static=BtnStateColor(text=Colors.YELLOW),
    hover=BtnStateColor(text=Colors.WHITE),
    click=BtnStateColor(text=Colors.ORANGE),
)
