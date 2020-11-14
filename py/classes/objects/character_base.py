from scenes.base import BaseScene as Scene
import pygame as pg
from lib.BasicObjects.health import Health


class Character:
    direction = {
        "up": (0, -1),
        "down": (0, 1),
        "right": (1, 0),
        "left": (-1, 0),
        "none": (0, 0)
    }

    def __init__(self, scene: Scene, image: pg.Surface, start_pos: tuple):
        self.scene = scene
        self.hp = Health()
        self.image = pg.transform.scale(image, (45, 45))
        self.rect = self.image.get_rect()
        self.shift_x = self.shift_y = 0
        self.change_pos(*start_pos)
        self.speed = 3

    def change_life(self, points):
        self.hp.change_count_lives(points)

    def change_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.x += self.shift_x * self.speed
        self.rect.y += self.shift_y * self.speed

    def set_dir(self, dir="none"):
        self.shift_x, self.shift_y = self.direction[dir]

    def draw(self):
        self.scene.screen.blit(self.image, self.rect)


