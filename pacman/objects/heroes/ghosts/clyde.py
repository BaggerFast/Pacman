from random import choice

from pacman.data_core.data_classes import GhostDifficult
from pacman.data_core.enums import GhostStateEnum
from pacman.misc.serializers import SettingsStorage
from pacman.scene_manager import SceneManager
from .base import Base, ghost_state


class Clyde(Base):
    seed_percent_in_home = 15
    love_point_in_scatter_mode = (0, 32)

    def __init__(self, game, loader, seed_count):
        super().__init__(game, loader, seed_count)
        self.set_direction("up")

    @ghost_state(GhostStateEnum.INDOOR)
    def home_ai(self, eaten_seed):
        super().home_ai(eaten_seed)
        if self.can_leave_home(eaten_seed):
            self.set_direction("left")
        if self.rect.centerx == self.room_center_pos[0]:
            self.set_direction("up")
        if self.rect.centery == self.door_room_pos[1]:
            self.state = GhostStateEnum.CHASE
            self.set_direction(choice(("left", "right")))

    @ghost_state(GhostStateEnum.CHASE)
    def chase_ai(self):
        pacman = SceneManager().current.pacman
        self.go_to_cell(pacman.get_cell())
        if self.two_cells_dis(self.get_cell(), pacman.get_cell()) <= 8:
            self.state = GhostStateEnum.SCATTER

    @ghost_state(GhostStateEnum.SCATTER)
    def scatter_ai(self):
        pacman = SceneManager().current.pacman
        if self.state is GhostStateEnum.SCATTER:
            self.go_to_cell(self.love_point_in_scatter_mode)
            if self.two_cells_dis(self.get_cell(), pacman.get_cell()) >= 8:
                self.state = GhostStateEnum.CHASE

    def generate_difficulty_settings(self) -> GhostDifficult:
        return (GhostDifficult(8000, 0, 0), GhostDifficult(4000, 0, 0), GhostDifficult(2000, 0, 0))[
            SettingsStorage().difficulty
        ]
