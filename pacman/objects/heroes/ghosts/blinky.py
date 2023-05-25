from random import choice

from pacman.data_core.data_classes import GhostDifficult
from pacman.data_core.enums import GhostStateEnum
from pacman.scenes import SceneManager
from pacman.storage import SettingsStorage

from .base import Base, ghost_state


class Blinky(Base):
    love_point_in_scatter_mode = (33, -3)

    def __init__(self, loader, seed_count):
        super().__init__(loader, seed_count)
        self.state = GhostStateEnum.CHASE
        self.set_direction(choice(("left", "right")))

    @ghost_state(GhostStateEnum.CHASE)
    def chase_ai(self):
        pacman = SceneManager().current.pacman
        self.go_to_cell(pacman.get_cell())
        if self.check_ai_timer(self.diffucult_settings.chase):
            self.state = GhostStateEnum.SCATTER

    @ghost_state(GhostStateEnum.SCATTER)
    def scatter_ai(self):
        self.go_to_cell(self.love_point_in_scatter_mode)
        if self.check_ai_timer(self.diffucult_settings.scatter):
            self.state = GhostStateEnum.CHASE

    def generate_difficulty_settings(self):
        return (
            GhostDifficult(8000, 20000, 6000),
            GhostDifficult(4000, 40000, 3000),
            GhostDifficult(2000, 80000, 1500),
        )[SettingsStorage().DIFFICULTY]
