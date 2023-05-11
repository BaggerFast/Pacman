import pygame as pg
from .base import Base
from ...data_core.enums import GhostStateEnum
from ...scene_manager import SceneManager


class Blinky(Base):
    love_point_in_scatter_mode = (33, -3)

    def __init__(self, game, loader, seed_count):
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
        super().__init__(game, loader, seed_count, frightened_time, chase_time, scatter_time)
        self.state = GhostStateEnum.SCATTER
        self.set_direction("left")

    def update(self) -> None:
        self.is_in_home = False
        if not self.is_invisible:
            super().update()
            self.collision = True
            self.go()

    @ghost_state(GhostStateEnum.SCATTER)
    def scatter_ai(self):
        self.go_to_cell(self.love_point_in_scatter_mode)
        if self.check_ai_timer(self.scatter_time):
            self.state = GhostStateEnum.CHASE

    @ghost_state(GhostStateEnum.CHASE)
    def chase_ai(self):
        pacman = SceneManager().current.pacman
        self.go_to_cell(pacman.get_cell())
        if self.check_ai_timer(self.chase_time):
            self.state = GhostStateEnum.SCATTER
