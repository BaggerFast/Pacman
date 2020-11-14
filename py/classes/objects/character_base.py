from scenes.base import BaseScene as Scene
import pygame as pg


class Character:
    def __init__(self, scene: Scene, image: pg.Surface, start_pos: tuple):
        self.image = image
        self.rect = self.image.get_rect()
        self.shift_x = self.shift_y = 0
        self.change_pos(*start_pos)
        self.scene = scene

    def change_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.x += self.shift_x
        self.rect.y += self.shift_y

    def check_event(self, event):
        if event.type == pg.KEYDOWN:
            pass

