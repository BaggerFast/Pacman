from typing import Tuple
from .base import Base
from misc import Rotation
from objects.character_base import Character
import pygame as pg


class Clyde(Base):
    max_count_eat_seeds_in_home = 60
    love_point_in_scatter_mode = (0, 32)

    def __init__(self, game, start_pos: Tuple[int, int], frightened_time=8000, chase_time=20000, scatter_time=7000):
        super().__init__(game, start_pos, frightened_time, chase_time, scatter_time)
        self.mode = 'Chase'
        self.set_direction(Rotation.up)

    def process_logic(self) -> None:
        if not self.is_invisible:
            super().process_logic()
            if self.is_in_home and self.can_leave_home():
                self.set_direction(Rotation.left)
                self.go()
                scene = self.game.current_scene
                if self.rect.centerx == scene.pinky.start_pos[0]:
                    self.set_direction(Rotation.up)
                if self.rect.centery == scene.blinky.start_pos[1]:
                    self.set_direction(Rotation.left)
                    self.is_in_home = False
                    self.collision = True

    def ghosts_ai(self) -> None:
        super().ghosts_ai()
        scene = self.game.current_scene
        pacman: Character = scene.pacman
        if self.mode == 'Scatter':
            self.love_cell = self.love_point_in_scatter_mode
            if self.cell.length_to(pacman.cell) >= 8:
                self.mode = 'Chase'
        if self.mode == 'Chase':
            self.love_cell = pacman.cell
            if self.cell.length_to(pacman.cell) <= 8:
                self.mode = 'Scatter'
