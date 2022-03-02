from abc import ABC
from typing import Tuple, List, Union

import pygame as pg

from misc import Animator
from misc.animator import SpriteSheetAnimator
from misc.constants import CELL_SIZE
from misc.interfaces.igeneric_object import IDrawable, ILogical
from objects.base import BaseObject


class Character(BaseObject, ILogical, IDrawable, ABC):
    direction = {
        "right": (1, 0, 0),
        "down": (0, 1, 1),
        "left": (-1, 0, 2),
        "up": (0, -1, 3),
    }

    def __init__(self, game, animator: Animator, start_pos: Tuple[int, int], aura: str = None) -> None:
        BaseObject.__init__(self)
        # todo delete game
        self.game = game
        self.__aura = pg.image.load(aura) if aura else aura
        self.animator: Animator = animator
        self.rect: pg.Rect = self.animator.current_image.get_rect()
        self.shift_x, self.shift_y = self.direction["right"][:2]
        self.start_pos: tuple = self.pos_from_cell(start_pos)
        self.move_center(*self.start_pos)
        self.speed: int = 0
        self.rotate: int = 0

    def step(self) -> None:
        self.rect.centerx = (self.rect.centerx + self.shift_x * self.speed + self.game.width) % self.game.width
        self.rect.centery = (self.rect.centery + self.shift_y * self.speed + self.game.height) % self.game.height

    def go(self) -> None:
        if self.speed:
            self.animator.start()
        self.speed = 1

    def stop(self) -> None:
        self.animator.stop()
        self.speed = 0

    def set_direction(self, new_direction: Union[str, int]) -> None:
        self.shift_x, self.shift_y, rotate = self.direction[new_direction]
        if self.rotate == rotate:
            return
        self.rotate = rotate
        if isinstance(self.animator, SpriteSheetAnimator):
            self.animator.rotate = rotate

    def process_logic(self) -> None:
        self.step()

    def process_draw(self, screen: pg.Surface) -> None:
        for i in range(-1, 2):
            if self.animator.current_aura:
                screen.blit(self.animator.current_aura, (self.rect.centerx - self.__aura.get_rect().width // 2,
                                                                   self.rect.centery - self.__aura.get_rect().height // 2))
            elif self.__aura:
                screen.blit(self.__aura, (self.rect.centerx - self.__aura.get_rect().width // 2,
                                                    self.rect.centery - self.__aura.get_rect().height // 2))
            screen.blit(self.animator.current_image, (self.rect.x + self.game.width * i, self.rect.y))

    def movement_cell(self, cell: Tuple[int, int]) -> list:
        scene = self.game.current_scene
        cell = scene.movements_data[cell[1]][cell[0]]
        return [i == '1' for i in "{0:04b}".format(cell)[::-1]]

    def move_to(self, direction) -> bool:
        return self.movement_cell(self.get_cell())[direction]

    def in_center(self) -> bool:
        return self.rect.centerx % CELL_SIZE == CELL_SIZE // 2 and (self.rect.centery - 20) % CELL_SIZE == CELL_SIZE // 2

    def get_cell(self) -> Tuple[int, int]:
        return self.rect.centerx // CELL_SIZE, (self.rect.centery - 20) // CELL_SIZE

    def in_rect(self, rect: List[int]) -> bool:
        return rect[0] <= self.get_cell()[0] <= rect[2] and rect[1] <= self.get_cell()[1] <= rect[3]

    @staticmethod
    def two_cells_dis(cell1: Tuple[int, int], cell2: Tuple[int, int]) -> float:
        return ((cell1[0] - cell2[0]) ** 2 + (cell1[1] - cell2[1]) ** 2) ** 0.5

    @staticmethod
    def pos_from_cell(cell: Tuple[int, int]) -> Tuple[int, int]:
        return cell[0] * CELL_SIZE + CELL_SIZE // 2, cell[1] * CELL_SIZE + 20 + CELL_SIZE // 2
