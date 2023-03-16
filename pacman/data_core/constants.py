import pygame as pg


class KbKeys:
    UP = [pg.K_UP, pg.K_w]
    DOWN = [pg.K_DOWN, pg.K_s]
    LEFT = [pg.K_LEFT, pg.K_d]
    RIGHT = [pg.K_RIGHT, pg.K_a]
    ENTER = [pg.K_SPACE, pg.K_RETURN]


class Colors:
    RED = pg.Color("red")
    BLUE = pg.Color("blue")
    GREEN = pg.Color("green")
    BLACK = pg.Color("black")
    WHITE = pg.Color("white")
    ORANGE = pg.Color("orange")
    YELLOW = pg.Color("yellow")
    GOLD = pg.Color("gold")
    GRAY = pg.Color("gray50")
    DARK_GRAY = pg.Color("gray26")
    SILVER = pg.Color(192, 192, 192)
    BRONZE = pg.Color(205, 127, 50)
    WOODEN = pg.Color(101, 67, 33)
    JET = pg.Color(10, 10, 10, 120)
    MAIN_MAP = pg.Color(33, 33, 255)
    DARK_RED = pg.Color(125, 0, 0)
    DARK_GREEN = pg.Color(0, 125, 0)
    HALF_TRANSPARENT = pg.Color(0, 0, 0, 40)
    TRANSPARENT = pg.Color(0, 0, 0, 0)
