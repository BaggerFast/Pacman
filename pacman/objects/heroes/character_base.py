from typing import List, Tuple

import pygame as pg

from pacman.animator import Animator, SpriteSheetAnimator
from pacman.data_core import Cfg, IDrawable, ILogical
from pacman.misc import CellUtil, LevelLoader, RectObj, load_image


class Character(RectObj, ILogical, IDrawable):
    direction = {
        "right": (1, 0, 0),
        "down": (0, 1, 1),
        "left": (-1, 0, 2),
        "up": (0, -1, 3),
        "none": (0, 0, None),
    }

    def __init__(self, animator: Animator, loader: LevelLoader, aura: str) -> None:
        super().__init__()
        self.level_loader = loader
        self.hero_pos = loader.heros_pos

        self.__aura = load_image(aura)
        self.animator = animator
        self.rect = self.animator.current_image.get_rect()
        self.shift_x, self.shift_y = self.direction["right"][:2]
        self.start_pos = CellUtil.get_center_pos(self.hero_pos[type(self).__name__.lower()])
        self.move_center(*self.start_pos)
        self.speed = 0
        self.rotate = 0

    def step(self) -> None:
        self.rect.centerx = (
            self.rect.centerx + self.shift_x * self.speed + Cfg.RESOLUTION.WIDTH
        ) % Cfg.RESOLUTION.WIDTH
        self.rect.centery = (
            self.rect.centery + self.shift_y * self.speed + Cfg.RESOLUTION.HEIGHT
        ) % Cfg.RESOLUTION.HEIGHT

    def go(self) -> None:
        if self.speed != 0:
            self.animator.start()
        self.speed = 1

    def stop(self) -> None:
        self.animator.stop()
        self.speed = 0

    def set_direction(self, new_direction="none") -> None:
        if not new_direction:
            return
        self.shift_x, self.shift_y, rotate = self.direction[new_direction]
        if self.rotate != rotate:
            self.rotate = rotate
            if isinstance(self.animator, SpriteSheetAnimator):
                self.animator.rotate(self.rotate)

    def update(self) -> None:
        self.step()

    def draw(self, screen: pg.Surface) -> None:
        for i in range(-1, 2):
            rect_x = self.rect.centerx - self.__aura.get_rect().width // 2
            rect_y = self.rect.centery - self.__aura.get_rect().height // 2
            screen.blit(self.__aura, (rect_x, rect_y))
            screen.blit(
                self.animator.current_image,
                (self.rect.x + Cfg.RESOLUTION.WIDTH * i, self.rect.y),
            )

    def movement_cell(self, cell: Tuple[int, int]) -> list:
        cell = self.level_loader.collision_map[cell[1]][cell[0]]
        return [bool(int(i)) for i in reversed("{0:04b}".format(cell))]

    def can_rotate_to(self, direction) -> bool:
        return self.movement_cell(self.get_cell())[direction]

    def get_cell(self) -> Tuple[int, int]:
        return CellUtil.get_cell(self.rect)

    def in_rect(self, rect: List[int]) -> bool:
        cell_x, cell_y = self.get_cell()
        return rect[0] <= cell_x <= rect[2] and rect[1] <= cell_y <= rect[3]

    @staticmethod
    def two_cells_dis(cell1: Tuple[int, int], cell2: Tuple[int, int]) -> float:
        return CellUtil.get_two_cells_dis(cell1, cell2)
