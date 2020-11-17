import pygame as pg

from lib.BasicObjects.health import Health
from scenes.base import BaseScene as Scene
from py.classes.objects.animator import Animator


class Character:
    direction = {
        "right": (1, 0, 0),
        "down": (0, 1, 1),
        "left": (-1, 0, 2),
        "up": (0, -1, 3),
        "none": (0, 0, None)
    }

    def __init__(self, scene: Scene, animator: Animator, start_pos: tuple):
        self.scene = scene
        self.hp = Health()
        self.animator = animator
        self.rect = self.animator.current_image.get_rect()
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
                self.animator.rotate = rotate
                self.animator.change_rotation()
        else:
            self.animator.rotate = self.rotate
            self.animator.change_rotation()

    def draw(self):
        self.scene.screen.blit(self.animator.current_image, self.rect)
