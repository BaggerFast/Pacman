from typing import List, Tuple
from .constants.variables import CELL_SIZE
from .vec import Vec


import pygame as pg


class BaseFromFileLoader:
    size = Vec(28, 31)

    def __init__(self, filename: str):
        self.filename: str = filename
        self.player_pos: Vec = Vec(0, 0)
        self.energizers_pos: List[Vec] = []
        self.seed_data: List[List[bool]] = \
            [[False for _ in range(self.size[0])]for _ in range(self.size[1])]
        self.movements_data: List[List[int]] = \
            [[False for _ in range(self.size[0])] for _ in range(self.size[1])]
        self.ghosts_pos: List[Vec] = []
        self.slow_ghost_rect: List[Tuple[int, int, int, int]] = []
        self.cant_up_ghost_rect: List[Tuple[int, int, int, int]] = []
        self.fruit_pos: Vec = Vec(0, 0)
        self.surface: pg.Surface = pg.Surface((self.size[0] * CELL_SIZE, self.size[1] * CELL_SIZE))

        self.load()
        self.clear_memory()

    def load(self): raise NotImplementedError  # вот тут все и загружается

    def get_file_name(self) -> str: return self.filename
    def get_movements_data(self) -> List[List[int]]: return self.movements_data
    def get_seed_data(self) -> List[List[bool]]: return self.seed_data
    def get_energizer_positions(self) -> List[Vec]: return self.energizers_pos
    def get_player_position(self) -> Vec: return self.player_pos
    def get_ghosts_positions(self) -> List[Vec]: return self.ghosts_pos
    def get_fruit_position(self) -> Vec: return self.fruit_pos
    def get_slow_ghost_rect(self) -> List[Tuple[int, int, int, int]]: return self.slow_ghost_rect
    def get_cant_up_ghost_rect(self) -> List[Tuple[int, int, int, int]]: return self.cant_up_ghost_rect

    def clear_memory(self): pass  # удаление лишних переменых, закрытие файлов
