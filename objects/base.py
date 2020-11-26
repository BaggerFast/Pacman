import pygame as pg
from abc import ABC, abstractmethod


class DrawableObject(ABC):
    def __init__(self, game):
        self.game = game
        self.rect = pg.rect.Rect(0, 0, 0, 0)

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move_center(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    @abstractmethod
    def process_event(self, event):
        pass

    @abstractmethod
    def process_logic(self):
        pass

    @abstractmethod
    def process_draw(self):
        pass  # use self.game.screen for drawing, padawan
