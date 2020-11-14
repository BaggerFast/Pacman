from scenes.base import BaseScene as Scene
import pygame as pg


class Character:
    def __init__(self, image, scene: Scene, start_pos: tuple):
        self.image = image
        self.scene = scene
        self.rect_collision = pg.Rect(0, 0, 50, 50)

    def update_pos(self, x, y):
        pass
