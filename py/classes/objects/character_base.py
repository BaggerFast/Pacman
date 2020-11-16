import pygame as pg

from lib.BasicObjects.health import Health
from scenes.base import BaseScene as Scene


class Character:
    direction = {
        "up": (0, -1, 3),
        "down": (0, 1, 1),
        "right": (1, 0, 0),
        "left": (-1, 0, 2),
        "none": (0, 0, None)
    }

    def __init__(self, scene: Scene, image: pg.Surface, start_pos: tuple):
        self.scene = scene
        self.hp = Health()
        self.image = image
        self.draw_image = self.image
        self.rect = self.image.get_rect()
        self.shift_x = self.shift_y = 0
        self.change_pos(*start_pos)
        self.speed = 1
        self.rotate = 0

    def change_life(self, points):
        self.hp.change_count_lives(points)

    def change_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.x = (self.rect.x + self.shift_x * self.speed
                       + self.scene.screen.get_width())\
                      % self.scene.screen.get_width()
        self.rect.y = (self.rect.y + self.shift_y * self.speed
                       + self.scene.screen.get_height())\
                      % self.scene.screen.get_height()

    def set_dir(self, dir="none"):
        if dir != "none":
            self.shift_x, self.shift_y, rotate = self.direction[dir]
            if self.rotate != rotate:
                self.rotate = rotate
                self.draw_image = pg.transform.rotate(self.image, -90 * rotate)
        else:
            self.draw_image = pg.transform.rotate(self.image, -90 * self.rotate)

    def draw(self):
        self.scene.screen.blit(self.draw_image, self.rect)
        self.scene.screen.blit(self.draw_image, (self.rect.x+self.scene.screen.get_width(), self.rect.y))
        self.scene.screen.blit(self.draw_image, (self.rect.x-self.scene.screen.get_width(), self.rect.y))
        self.scene.screen.blit(self.draw_image, (self.rect.x, self.rect.y+self.scene.screen.get_height()))
        self.scene.screen.blit(self.draw_image, (self.rect.x, self.rect.y-self.scene.screen.get_height()))
