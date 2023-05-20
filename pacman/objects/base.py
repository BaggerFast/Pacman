from pygame import Rect


class MovementObject:
    def __init__(self):
        self.rect = Rect(0, 0, 0, 0)

    def move(self, x, y) -> "MovementObject":
        self.rect.x, self.rect.y = x, y
        return self

    def move_center(self, x: int, y: int) -> "MovementObject":
        self.rect.centerx, self.rect.centery = x, y
        return self
