import pygame as pg
from pygame import Surface

from pacman.data_core import GameObjects
from pacman.data_core.enums import FruitStateEnum
from pacman.data_core.interfaces import IDrawable, ILogical
from pacman.misc.animator.sprite_sheet import sprite_slice
from pacman.misc.cell_util import CellUtil
from pacman.objects import ImageObject, Text
from pacman.objects.base import MovementObject


class Fruit(MovementObject, IDrawable, ILogical):
    def __init__(self, pos: tuple) -> None:
        super().__init__()
        self.__fruit_sprite = list(sprite_slice("fruits", (12, 12)))[::-1]
        self.rect = self.__fruit_sprite[0].get_rect()
        self.move_center(*CellUtil.center_pos_from_cell(pos))
        self.state = FruitStateEnum.DISABLED

        self.timer = pg.time.get_ticks()
        self.eaten_text = Text(f" ", 10, self.rect)
        self.eaten_fruits_hud = GameObjects()

    def change_state(self, state: FruitStateEnum):
        self.state = state
        self.timer = pg.time.get_ticks()

    def toggle_mode_to_eaten(self, score):
        if not self.__fruit_sprite:
            return
        self.eaten_text.text = f"{score}"
        x_offset = len(self.eaten_fruits_hud)
        pos_x_hud = 130 + x_offset + x_offset * self.rect.width
        self.eaten_fruits_hud.append(ImageObject(self.__fruit_sprite.pop(), (pos_x_hud, 270)))
        self.change_state(FruitStateEnum.EATEN)

    def process_collision(self, rect: pg.Rect) -> bool:
        return self.state == FruitStateEnum.ACTIVE and self.rect.center == rect.center and self.__fruit_sprite

    def update(self):
        if self.state is FruitStateEnum.DISABLED and pg.time.get_ticks() - self.timer >= 9000:
            self.change_state(FruitStateEnum.ACTIVE)
        elif self.state is FruitStateEnum.EATEN and pg.time.get_ticks() - self.timer >= 500:
            self.change_state(FruitStateEnum.DISABLED)

    def draw(self, screen: Surface) -> None:
        if self.state is FruitStateEnum.ACTIVE and self.__fruit_sprite:
            sprite = self.__fruit_sprite[len(self.__fruit_sprite) - 1]
            screen.blit(sprite, self.rect)
        elif self.state is FruitStateEnum.EATEN:
            self.eaten_text.draw(screen)
        self.eaten_fruits_hud.draw(screen)
