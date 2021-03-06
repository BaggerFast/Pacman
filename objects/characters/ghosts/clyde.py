from typing import Tuple
from .base import Base
from .ghost_states import GhostState


class Clyde(Base):
    max_count_eat_seeds_in_home = 60
    love_point_in_scatter_mode = (0, 32)

    def __init__(self, game, start_pos: Tuple[int, int], frightened_time=8000, chase_time=20000, scatter_time=7000):
        super().__init__(game, start_pos, frightened_time, chase_time, scatter_time)
        self.mode = GhostState.chase
        self.shift_y = 1
        self.set_direction('up')

    # region Public

    # region Implementation of parent class

    def process_logic(self) -> None:
        if not self.is_invisible:
            super().process_logic()
            if self.is_in_home and self.can_leave_home:
                self.set_direction("left")
                self.go()
                scene = self.game.current_scene
                if self.rect.centerx == scene.pinky.start_pos[0]:
                    self.set_direction("up")
                if self.rect.centery == scene.blinky.start_pos[1]:
                    self.set_direction("left")
                    self.is_in_home = False
                    self.collision = True

    # endregion

    def ghosts_ai(self) -> None:
        super().ghosts_ai()
        scene = self.game.current_scene
        pacman = scene.pacman
        if self.mode == GhostState.scatter:
            self.love_cell = self.love_point_in_scatter_mode
            if self.two_cells_dis(self.get_cell(), pacman.get_cell()) >= 8:
                self.mode = GhostState.chase
        elif self.mode == GhostState.chase:
            self.love_cell = pacman.get_cell()
            if self.two_cells_dis(self.get_cell(), pacman.get_cell()) <= 8:
                self.mode = GhostState.scatter

    def set_difficult(self, difficult):
        data = {
            0: [8000, 0, 0],
            1: [4000, 0, 0],
            2: [2000, 0, 0],
        }
        if difficult in data:
            self.set_power(*data[difficult])

    # endregion
