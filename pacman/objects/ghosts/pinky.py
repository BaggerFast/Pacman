from typing import Tuple
import pygame as pg
from .base import Base
from ...data_core.enums import GhostStateEnum
from ...misc.serializers import SettingsStorage


class Pinky(Base):
    love_point_in_scatter_mode = (2, -3)

    def __init__(
        self,
        game,
        start_pos: Tuple[int, int],
        seed_count,
    ):
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
        self.shift_y = -1
        self.set_direction("down")

    def home_ai(self, eaten_seed):
        super().home_ai(eaten_seed)
        if self.can_leave_home(eaten_seed):
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
        if self.state is GhostStateEnum.SCATTER:
            self.love_cell = self.love_point_in_scatter_mode
            if pg.time.get_ticks() - self.ai_timer >= self.scatter_time:
                self.update_ai_timer()
                self.state = GhostStateEnum.CHASE
        if self.state is GhostStateEnum.CHASE:
            rotate = pacman.rotate
            self.love_cell = (
                pacman.get_cell()[0] + self.direction2[rotate][0] * 2,
                pacman.get_cell()[1] + self.direction2[rotate][1] * 2,
            )
            if pg.time.get_ticks() - self.ai_timer >= self.chase_time:
                self.update_ai_timer()
                self.state = GhostStateEnum.SCATTER
