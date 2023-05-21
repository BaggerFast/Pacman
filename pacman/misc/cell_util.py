from abc import ABC
from math import hypot
from typing import Final, Tuple

from pygame import Rect

from pacman.data_core import Cfg


class CellUtil(ABC):
    OFFSET_Y: Final = 20

    @classmethod
    def get_center_pos(cls, cell: Tuple[int, int]) -> Tuple[int, int]:
        return cell[0] * Cfg.TILE_SIZE + Cfg.TILE_SIZE // 2, cell[1] * Cfg.TILE_SIZE + cls.OFFSET_Y + Cfg.TILE_SIZE // 2

    @staticmethod
    def get_two_cells_dis(cell1: Tuple[int, int], cell2: Tuple[int, int]) -> float:
        return hypot(cell1[0] - cell2[0], cell1[1] - cell2[1])

    @classmethod
    def get_cell(cls, rect: Rect) -> Tuple[int, int]:
        return rect.centerx // Cfg.TILE_SIZE, (rect.centery - cls.OFFSET_Y) // Cfg.TILE_SIZE

    @classmethod
    def is_in_cell_center(cls, rect: Rect) -> bool:
        half_cell = Cfg.TILE_SIZE // 2
        return rect.centerx % Cfg.TILE_SIZE == half_cell and (rect.centery - cls.OFFSET_Y) % Cfg.TILE_SIZE == half_cell
