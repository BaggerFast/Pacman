import pygame
from random import randint

from objects.base import DrawObject


class Ball(DrawObject):
    filename = 'images/basketball.png'

    def __init__(self, game, x=100, y=100):
        super().__init__(game)
        self.image = pygame.image.load(Ball.filename)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.x = x
        self.y = y

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)


class LinearMovingBall(Ball):
    def __init__(self, game):
        super().__init__(game)
        self.window_width = self.game.width
        self.window_height = self.game.height
        self.rect.x = randint(10, self.window_width - self.rect.width - 10)
        self.rect.y = randint(10, self.window_height - self.rect.height - 10)
        self.shift_x = 1 if randint(0, 1) == 1 else -1
        self.shift_y = 1 if randint(0, 1) == 1 else -1

    def process_logic(self):
        self.rect.x += self.shift_x
        self.rect.y += self.shift_y
        if self.rect.left <= 0 or self.rect.right >= self.window_width:
            self.shift_x *= -1
            self.game.wall_collision_count += 1
        if self.rect.top <= 0 or self.rect.bottom >= self.window_height:
            self.shift_y *= -1
            self.game.wall_collision_count += 1

    def collides_with(self, other_ball):
        return pygame.sprite.collide_mask(self, other_ball)

    def collision(self, other_ball):
        self.shift_x, other_ball.shift_x = other_ball.shift_x, self.shift_x
        self.shift_y, other_ball.shift_y = other_ball.shift_y, self.shift_y