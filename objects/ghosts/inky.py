from typing import Tuple
from .base import Base
import pygame as pg


class Inky(Base):
    max_count_eat_seeds_in_home = 30
    love_point_in_scatter_mode = (27, 32)

    def __init__(self, game, start_pos: Tuple[int, int], frightened_time=8000, chase_time=20000, scatter_time=5000):
        super().__init__(game, start_pos, frightened_time, chase_time, scatter_time)
        self.shift_y = 1
        self.set_direction('up')

    def process_logic(self) -> None:
        if not self.is_invisible:
            super().process_logic()
            if self.is_in_home and self.can_leave_home():
                self.set_direction("right")
                self.go()
                scene = self.game.current_scene
                if self.rect.centerx == scene.pinky.start_pos[0]:
                    self.set_direction("up")
                if self.rect.centery == scene.blinky.start_pos[1]:
                    self.set_direction("left")
                    self.is_in_home = False
                    self.collision = True

    def ghosts_ai(self) -> None:
        super().ghosts_ai()
        scene = self.game.current_scene
        pacman = scene.pacman
        blinky = scene.blinky
        if self.mode == 'Scatter':
            self.love_cell = self.love_point_in_scatter_mode
            if pg.time.get_ticks() - self.ai_timer >= self.scatter_time:
                self.update_ai_timer()
                self.mode = 'Chase'
        if self.mode == 'Chase':
            pacman_cell = pacman.get_cell()
            rotate = pacman.rotate
            blinky_cell = blinky.get_cell()
            pinky_love_cell = (
                pacman_cell[0] + self.direction2[rotate][0] * 2,
                pacman_cell[1] + self.direction2[rotate][1] * 2
            )
            vector_blinky_cell_pinky_love_cell = (
                blinky_cell[0] - pinky_love_cell[0],
                blinky_cell[1] - pinky_love_cell[1]
            )
            self.love_cell = (
                pinky_love_cell[0] + vector_blinky_cell_pinky_love_cell[0],
                pinky_love_cell[1] + vector_blinky_cell_pinky_love_cell[1]
            )
            if pg.time.get_ticks() - self.ai_timer >= self.chase_time:
                self.update_ai_timer()
                self.mode = 'Scatter'
