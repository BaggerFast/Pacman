from random import choice
from .base import Base, ghost_state
from ...data_core.data_classes import GhostDifficult
from ...data_core.enums import GhostStateEnum
from ...misc.serializers import SettingsStorage
from ...scene_manager import SceneManager


class Pinky(Base):
    love_point_in_scatter_mode = (2, -3)

    def __init__(self, game, loader, seed_count):
        super().__init__(game, loader, seed_count)
        self.shift_y = -1
        self.set_direction("down")

    @ghost_state(GhostStateEnum.INDOOR)
    def home_ai(self, eaten_seed):
        super().home_ai(eaten_seed)
        if self.can_leave_home(eaten_seed):
            self.set_direction("up")
        if self.rect.centery == self.blinky_start_pos[1]:
            self.state = GhostStateEnum.SCATTER
            self.set_direction(choice(("left", "right")))

    @ghost_state(GhostStateEnum.SCATTER)
    def scatter_ai(self):
        self.go_to_cell(self.love_point_in_scatter_mode)
        if self.check_ai_timer(self.diffucult_settings.scatter):
            self.state = GhostStateEnum.CHASE

    @ghost_state(GhostStateEnum.CHASE)
    def chase_ai(self):
        pacman = SceneManager().current.pacman
        rotate = pacman.rotate
        self.go_to_cell(
            (
                pacman.get_cell()[0] + self.direction2[rotate][0] * 2,
                pacman.get_cell()[1] + self.direction2[rotate][1] * 2,
            )
        )
        if self.check_ai_timer(self.diffucult_settings.chase):
            self.state = GhostStateEnum.SCATTER

    def generate_difficulty_settings(self) -> GhostDifficult:
        return (
            GhostDifficult(8000, 20000, 7000),
            GhostDifficult(4000, 40000, 5000),
            GhostDifficult(2000, 80000, 3000),
        )[SettingsStorage().difficulty]
