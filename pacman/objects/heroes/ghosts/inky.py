from random import choice

from pacman.data_core.data_classes import GhostDifficult
from pacman.data_core.enums import GhostStateEnum
from pacman.scenes import SceneManager
from pacman.storage import SettingsStorage

from .base import Base, ghost_state


class Inky(Base):
    seed_percent_in_home = 8
    love_point_in_scatter_mode = (27, 32)

    def __init__(self, loader, seed_count):
        super().__init__(loader, seed_count)
        self.set_direction("up")

    @ghost_state(GhostStateEnum.INDOOR)
    def home_ai(self, eaten_seed):
        super().home_ai(eaten_seed)
        if self.can_leave_home(eaten_seed):
            self.set_direction("right")
        if self.rect.centerx == self.room_center_pos[0]:
            self.set_direction("up")
        if self.rect.centery == self.door_room_pos[1]:
            self.set_direction(choice(("left", "right")))
            self.state = GhostStateEnum.CHASE

    @ghost_state(GhostStateEnum.CHASE)
    def chase_ai(self):
        pacman = SceneManager().current.pacman
        blinky = SceneManager().current.blinky
        pacman_cell = pacman.get_cell()
        rotate = pacman.rotate
        blinky_cell = blinky.get_cell()
        pinky_love_cell = (
            pacman_cell[0] + self.direction2[rotate][0] * 2,
            pacman_cell[1] + self.direction2[rotate][1] * 2,
        )
        vector_blinky_cell_pinky_love_cell = (
            blinky_cell[0] - pinky_love_cell[0],
            blinky_cell[1] - pinky_love_cell[1],
        )
        self.go_to_cell(
            (
                pinky_love_cell[0] + vector_blinky_cell_pinky_love_cell[0],
                pinky_love_cell[1] + vector_blinky_cell_pinky_love_cell[1],
            )
        )
        if self.check_ai_timer(self.diffucult_settings.chase):
            self.state = GhostStateEnum.SCATTER

    @ghost_state(GhostStateEnum.SCATTER)
    def scatter_ai(self):
        self.go_to_cell(self.love_point_in_scatter_mode)
        if self.check_ai_timer(self.diffucult_settings.scatter):
            self.state = GhostStateEnum.CHASE

    def generate_difficulty_settings(self) -> GhostDifficult:
        return (
            GhostDifficult(8000, 20000, 5000),
            GhostDifficult(4000, 40000, 3000),
            GhostDifficult(2000, 80000, 1000),
        )[SettingsStorage().DIFFICULTY]
