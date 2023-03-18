from abc import ABC
from typing import Tuple, Final
import pygame as pg


class CellUtil(ABC):
    CELL_SIZE: Final[int] = 8

    @classmethod
    def pos_from_cell(cls, cell: Tuple[int, int]) -> Tuple[int, int]:
        return cell[0] * cls.CELL_SIZE + cls.CELL_SIZE // 2, cell[1] * cls.CELL_SIZE + 20 + cls.CELL_SIZE // 2

    @staticmethod
    def two_cells_dis(cell1: Tuple[int, int], cell2: Tuple[int, int]) -> float:
        return ((cell1[0] - cell2[0]) ** 2 + (cell1[1] - cell2[1]) ** 2) ** 0.5

    @classmethod
    def get_cell(cls, rect: pg.Rect) -> Tuple[int, int]:
        return rect.centerx // cls.CELL_SIZE, (rect.centery - 20) // cls.CELL_SIZE

    @classmethod
    def in_cell_center(cls, rect: pg.Rect) -> bool:
        half_cell = cls.CELL_SIZE // 2
        return rect.centerx % cls.CELL_SIZE == half_cell and (rect.centery - 20) % cls.CELL_SIZE == half_cell
