from typing import Tuple
from .base import Base
from misc import Rotation, vec
from objects.character_base import Character
import pygame as pg


class Inky(Base):
    max_count_eat_seeds_in_home = 30
    love_point_in_scatter_mode = (27, 32)

    def __init__(self, game, start_pos: Tuple[int, int], frightened_time=8000, chase_time=20000, scatter_time=5000):
        super().__init__(game, start_pos, frightened_time, chase_time, scatter_time)
        self.set_direction(Rotation.up)

    def process_logic(self) -> None:
        if not self.is_invisible:
            super().process_logic()
            if self.is_in_home and self.can_leave_home():
                self.set_direction(Rotation.right)
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
        blinky: Character = scene.blinky
        if self.mode == 'Scatter':
            self.love_cell = self.love_point_in_scatter_mode
            if pg.time.get_ticks() - self.ai_timer >= self.scatter_time:
                self.update_ai_timer()
                self.mode = 'Chase'
        if self.mode == 'Chase':
            pinky_love_cell: vec = pacman.cell.offset(pacman.rotate, 2)
            self.love_cell = pinky_love_cell - (blinky.cell - pinky_love_cell)
            if pg.time.get_ticks() - self.ai_timer >= self.chase_time:
                self.update_ai_timer()
                self.mode = 'Scatter'
