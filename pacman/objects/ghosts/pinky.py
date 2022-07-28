from typing import Tuple
from .base import Base
import pygame as pg


class Pinky(Base):
    love_point_in_scatter_mode = (2, -3)

    def __init__(self, game, start_pos: Tuple[int, int], frightened_time=8000, chase_time=20000, scatter_time=7000):
        super().__init__(game, start_pos, frightened_time, chase_time, scatter_time)
        self.shift_y = -1
        self.set_direction('down')

    def process_logic(self) -> None:
        if not self.is_invisible:
            super().process_logic()
            if self.is_in_home and self.can_leave_home():
                self.set_direction("up")
                self.go()
                scene = self.game.current_scene
                if self.rect.centery == scene.blinky.start_pos[1]:
                    self.set_direction("left")
                    self.is_in_home = False
                    self.collision = True

    def ghosts_ai(self) -> None:
        super().ghosts_ai()
        scene = self.game.current_scene
        pacman = scene.pacman
        if self.mode == 'Scatter':
            self.love_cell = self.love_point_in_scatter_mode
            if pg.time.get_ticks() - self.ai_timer >= self.scatter_time:
                self.update_ai_timer()
                self.mode = 'Chase'
        if self.mode == 'Chase':
            rotate = pacman.rotate
            self.love_cell = (
                pacman.get_cell()[0]+self.direction2[rotate][0]*2,
                pacman.get_cell()[1]+self.direction2[rotate][1]*2
            )
            if pg.time.get_ticks() - self.ai_timer >= self.chase_time:
                self.update_ai_timer()
                self.mode = 'Scatter'
