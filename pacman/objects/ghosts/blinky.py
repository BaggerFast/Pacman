from random import choice
from .base import Base, ghost_state
from ...data_core.data_classes import GhostDifficult
from ...data_core.enums import GhostStateEnum
from ...misc.serializers import SettingsStorage
from ...scene_manager import SceneManager


class Blinky(Base):
    love_point_in_scatter_mode = (33, -3)

    def __init__(self, game, loader, seed_count):
        super().__init__(game, loader, seed_count)
        self.state = GhostStateEnum.SCATTER
        self.set_direction(choice(("left", "right")))
        self.go()

    @ghost_state(GhostStateEnum.SCATTER)
    def scatter_ai(self):
        self.go_to_cell(self.love_point_in_scatter_mode)
        if self.check_ai_timer(self.diffucult_settings.scatter):
            self.state = GhostStateEnum.CHASE

    @ghost_state(GhostStateEnum.CHASE)
    def chase_ai(self):
        pacman = SceneManager().current.pacman
        self.go_to_cell(pacman.get_cell())
        if self.check_ai_timer(self.diffucult_settings.chase):
            self.state = GhostStateEnum.SCATTER

    def generate_difficulty_settings(self):
        return (
            GhostDifficult(8000, 20000, 7000),
            GhostDifficult(4000, 40000, 5000),
            GhostDifficult(2000, 80000, 3000),
        )[SettingsStorage().difficulty]
