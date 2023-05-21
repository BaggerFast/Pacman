from pygame import Rect


class RectObj:
    def __init__(self, rect: Rect = Rect(0, 0, 0, 0)):
        self.rect = rect

    def move(self, x, y) -> "RectObj":
        self.rect.x, self.rect.y = x, y
        return self

    def move_center(self, x: int, y: int) -> "RectObj":
        self.rect.centerx, self.rect.centery = x, y
        return self
