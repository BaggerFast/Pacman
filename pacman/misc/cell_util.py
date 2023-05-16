from abc import ABC
from math import hypot
from typing import Tuple, Final

import pygame as pg


class CellUtil(ABC):
    CELL_SIZE: Final[int] = 8
    OFFSET_Y = 20

    @classmethod
    def center_pos_from_cell(cls, cell: Tuple[int, int]) -> Tuple[int, int]:
        return cell[0] * cls.CELL_SIZE + cls.CELL_SIZE // 2, cell[1] * cls.CELL_SIZE + cls.OFFSET_Y + cls.CELL_SIZE // 2

    @staticmethod
    def two_cells_dis(cell1: Tuple[int, int], cell2: Tuple[int, int]) -> float:
        return hypot(cell1[0] - cell2[0], cell1[1] - cell2[1])

    @classmethod
    def get_cell(cls, rect: pg.Rect) -> Tuple[int, int]:
        return rect.centerx // cls.CELL_SIZE, (rect.centery - cls.OFFSET_Y) // cls.CELL_SIZE

    @classmethod
    def in_cell_center(cls, rect: pg.Rect) -> bool:
        half_cell = cls.CELL_SIZE // 2
        return rect.centerx % cls.CELL_SIZE == half_cell and (rect.centery - cls.OFFSET_Y) % cls.CELL_SIZE == half_cell
