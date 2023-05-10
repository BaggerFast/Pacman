from .base import Base
from ...data_core.enums import GhostStateEnum
from ...misc.serializers import SettingsStorage
from ...scene_manager import SceneManager


class Clyde(Base):
    seed_percent_in_home = 15
    love_point_in_scatter_mode = (0, 32)

    def __init__(self, game, loader, seed_count):
        frightened_time = 8000
        chase_time = 0
        scatter_time = 0
        if SettingsStorage().difficulty == 1:
            frightened_time = 4000
            chase_time = 0
            scatter_time = 0
        elif SettingsStorage().difficulty == 2:
            frightened_time = 2000
            chase_time = 0
            scatter_time = 0
        super().__init__(game, loader, seed_count, frightened_time, chase_time, scatter_time)
        self.state = GhostStateEnum.CHASE
        self.shift_y = 1
        self.set_direction("up")

    def home_ai(self, eaten_seed):
        super().home_ai(eaten_seed)
        if self.can_leave_home(eaten_seed):
            self.set_direction("left")
            self.go()
            if self.rect.centerx == self.pinky_start_pos[0]:
                self.set_direction("up")
            if self.rect.centery == self.blinky_start_pos[1]:
                self.set_direction("left")
                self.is_in_home = False
                self.collision = True

    def ghosts_ai(self) -> None:
        super().ghosts_ai()
        pacman = SceneManager().current.pacman
        if self.state is GhostStateEnum.SCATTER:
            self.love_cell = self.love_point_in_scatter_mode
            if self.two_cells_dis(self.get_cell(), pacman.get_cell()) >= 8:
                self.state = GhostStateEnum.CHASE
        elif self.state is GhostStateEnum.CHASE:
            self.love_cell = pacman.get_cell()
            if self.two_cells_dis(self.get_cell(), pacman.get_cell()) <= 8:
                self.state = GhostStateEnum.SCATTER
