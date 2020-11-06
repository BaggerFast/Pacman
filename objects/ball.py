import pygame

from misc import get_nonzero_random_value
from objects.image import ImageObject


class BallObject(ImageObject):
    filename = 'images/basketball.png'
    image = pygame.image.load(filename)
    MAX_SPEED = 2

    def __init__(self, game, x: int = 0, y: int = 0, speed: int = None) -> None:
        super().__init__(game)
        self.rect.x = x
        self.rect.y = y
        self.radius = self.rect.width // 2
        self.speed = speed if speed else [
            get_nonzero_random_value(BallObject.MAX_SPEED),
            get_nonzero_random_value(BallObject.MAX_SPEED)
        ]

    def collides_with(self, other) -> bool:
        return pygame.sprite.collide_circle(self, other)

    def bounce(self, other) -> None:
        self.speed, other.speed = other.speed, self.speed

    def vertical_edge_collision(self) -> bool:
        return self.rect.right >= self.game.WIDTH or self.rect.left <= 0

    def horisontal_edge_collision(self) -> bool:
        return self.rect.bottom >= self.game.HEIGHT or self.rect.top <= 0

    def edge_collision(self) -> bool:
        return self.horisontal_edge_collision() or self.vertical_edge_collision()

    def check_borders(self) -> None:
        if self.vertical_edge_collision():
            self.speed[0] *= -1
        if self.horisontal_edge_collision():
            self.speed[1] *= -1

    def step(self) -> None:
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def process_logic(self) -> None:
        self.check_borders()
        self.step()
