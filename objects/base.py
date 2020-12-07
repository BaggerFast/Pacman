import pygame as pg


class DrawableObject:
    def __init__(self, game, is_hidden=False) -> None:
        self.game = game
        self.is_hidden = is_hidden
        self.rect = pg.rect.Rect(0, 0, 0, 0)

    def move(self, x, y) -> None:
        self.rect.x = x
        self.rect.y = y

    def move_center(self, x: int, y: int) -> None:
        self.rect.centerx = x
        self.rect.centery = y

    def process_event(self, event: pg.event.Event) -> None:
        pass

    def process_logic(self) -> None:
        pass

    def process_draw(self) -> None:
        """
        Use self.game.screen for drawing, padawan
        """
        pass
