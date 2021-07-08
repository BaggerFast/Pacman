import pygame as pg
from misc import CELL_SIZE, Animator, TilePos, Rotation
from objects import DrawableObject
from typing import Tuple, List, Union


class Character(DrawableObject):
    def __init__(self, game, animator: Animator, start_pos: Union[Tuple[int, int], TilePos], aura: str = None):
        super().__init__(game)
        self.__aura = pg.image.load(aura) if aura else aura
        self.animator: Animator = animator
        self.rect: pg.Rect = self.animator.current_image.get_rect()
        self.start_pos: tuple = self.pos_from_cell(start_pos)
        self.move_center(*self.start_pos)
        self.speed: int = 0
        self.rotate: Rotation = Rotation.right

    @property
    def shift(self) -> Tuple[int, int]: return self.rotate.offset

    @property
    def shift_x(self) -> int: return self.rotate.x_offset

    @property
    def shift_y(self) -> int: return self.rotate.y_offset

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

    def set_direction(self, new_direction) -> None:
        if self.rotate == new_direction:
            return
        self.rotate = new_direction
        self.animator.rotate = new_direction
        if self.animator.is_rotation:
            self.animator.change_rotation()

    def process_logic(self) -> None: self.step()

    def process_draw(self) -> None:
        for i in range(-1, 2):
            if self.animator.current_aura:
                self.game.screen.blit(self.animator.current_aura, self.animator.current_aura.get_rect(center=self.rect.center))
            elif self.__aura:
                self.game.screen.blit(self.__aura, self.__aura.get_rect(center=self.rect.center))
            self.game.screen.blit(self.animator.current_image, (self.rect.x + self.game.width * i, self.rect.y))

    def movement_cell(self, cell: Union[Tuple[int, int], TilePos]) -> List:
        scene = self.game.current_scene
        cell = scene.movements_data[cell[1]][cell[0]]
        return [i == '1' for i in "{0:04b}".format(cell)[::-1]]

    def move_to(self, direction: Union[int, Rotation]) -> bool: return self.movement_cell(self.get_cell())[direction]

    def in_center(self) -> bool:
        return self.rect.centerx % CELL_SIZE == CELL_SIZE // 2 \
               and (self.rect.centery - 20) % CELL_SIZE == CELL_SIZE // 2

    def get_cell(self) -> TilePos: return TilePos(self.rect.centerx // CELL_SIZE, (self.rect.centery - 20) // CELL_SIZE)

    @property
    def cell(self) -> TilePos: return self.get_cell()

    def in_rect(self, rect: Union[List[int], pg.Rect]) -> bool:
        return rect[0] <= self.get_cell()[0] <= rect[2] and rect[1] <= self.get_cell()[1] <= rect[3]

    @staticmethod
    def two_cells_dis(cell1: Tuple[int, int], cell2: Tuple[int, int]) -> float:
        return ((cell1[0] - cell2[0]) ** 2 + (cell1[1] - cell2[1]) ** 2) ** 0.5

    @staticmethod
    def pos_from_cell(cell: Union[Tuple[int, int], TilePos]) -> Tuple[int, int]:
        return int(cell[0] * CELL_SIZE + CELL_SIZE // 2), int(cell[1] * CELL_SIZE + 20 + CELL_SIZE // 2)
