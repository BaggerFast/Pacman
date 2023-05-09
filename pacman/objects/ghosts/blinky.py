from typing import Tuple
import pygame as pg
from .base import Base
from ...data_core.enums import GhostStateEnum
from ...misc.serializers import SettingsStorage
from ...scene_manager import SceneManager


class Blinky(Base):
    love_point_in_scatter_mode = (33, -3)

    def __init__(self, game, start_pos: Tuple[int, int], seed_count):
        frightened_time = 8000
        chase_time = 20000
        scatter_time = 7000
        if SettingsStorage().difficulty == 1:
            frightened_time = 4000
            chase_time = 40000
            scatter_time = 5000
        elif SettingsStorage().difficulty == 2:
            frightened_time = 2000
            chase_time = 80000
            scatter_time = 3000
        super().__init__(game, start_pos, seed_count, frightened_time, chase_time, scatter_time)
        self.state = GhostStateEnum.SCATTER
        self.set_direction("left")

    def update(self) -> None:
        self.is_in_home = False
        if not self.is_invisible:
            super().update()
            self.collision = True
            self.go()

    def ghosts_ai(self) -> None:
        super().ghosts_ai()
        scene = SceneManager().current
        pacman = scene.pacman
        if self.state is GhostStateEnum.SCATTER:
            self.love_cell = self.love_point_in_scatter_mode
            if pg.time.get_ticks() - self.ai_timer >= self.scatter_time:
                self.update_ai_timer()
                self.state = GhostStateEnum.CHASE
        if self.state is GhostStateEnum.CHASE:
            self.love_cell = pacman.get_cell()
            if pg.time.get_ticks() - self.ai_timer >= self.chase_time:
                self.update_ai_timer()
                self.state = GhostStateEnum.SCATTER
