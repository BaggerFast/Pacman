from typing import Tuple
import pygame as pg
from objects.characters.ghosts.base import Base
from objects.characters.ghosts.ghost_states import GhostState


class Blinky(Base):
    love_point_in_scatter_mode = (33, -3)

    def __init__(self, game, start_pos: Tuple[int, int], frightened_time=8000, chase_time=20000, scatter_time=7000):
        super().__init__(game, start_pos, frightened_time, chase_time, scatter_time)
        self.mode = GhostState.scatter
        self.set_direction('left')

    # region Public

    # region Implementation of parent class

    def process_logic(self) -> None:
        self.is_in_home = False
        if not self.is_invisible:
            super().process_logic()
            self.collision = True
            self.go()

    # endregion

    def ghosts_ai(self) -> None:
        super().ghosts_ai()
        scene = self.game.scene_manager.current
        pacman = scene.pacman
        if self.mode == GhostState.scatter:
            self.love_cell = self.love_point_in_scatter_mode
            if pg.time.get_ticks() - self.ai_timer >= self.scatter_time:
                self.update_ai_timer()
                self.mode = GhostState.chase
        if self.mode == GhostState.chase:
            self.love_cell = pacman.get_cell()
            if pg.time.get_ticks() - self.ai_timer >= self.chase_time:
                self.update_ai_timer()
                self.mode = GhostState.scatter

    def set_difficult(self, difficult):
        # todo improve difficult system
        data = {
            0: [8000, 20000, 7000],
            1: [4000, 40000, 5000],
            2: [2000, 80000, 3000],
        }
        if difficult in data:
            self.set_power(*data[difficult])

    # endregion
