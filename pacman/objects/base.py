import pygame as pg


class DrawableObject:
    def __init__(self, is_hidden=False) -> None:
        self.is_hidden = is_hidden
        self.rect = pg.rect.Rect(0, 0, 0, 0)

    def move(self, x, y) -> "DrawableObject":
        self.rect.x, self.rect.y = x, y
        return self

    def move_center(self, x: int, y: int) -> "DrawableObject":
        self.rect.centerx, self.rect.centery = x, y
        return self

    # todo: DELETE
    def process_event(self, event: pg.event.Event) -> None:
        pass

    def process_logic(self) -> None:
        pass

    def process_draw(self, screen: pg.Surface) -> None:
        pass
