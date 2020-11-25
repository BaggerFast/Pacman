from misc.animator import Animator
from misc.path import get_image_path_for_animator
from objects.character_base import Character
from objects.ghosts.base_ghost import BaseGhost


class Blinky(BaseGhost):

    def __init__(self, game, start_pos: tuple):
        self.top_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'blinky', 'top'), is_rotation=False
        )
        self.bottom_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'blinky', 'bottom'),  is_rotation=False
        )
        self.left_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'blinky', 'left'), is_rotation=False
        )
        self.right_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'blinky', 'right'), is_rotation=False
        )
        self.animations = {
            3: self.top_walk_anim,
            2: self.left_walk_anim,
            1: self.bottom_walk_anim,
            0: self.right_walk_anim
        }

        super().__init__(game, self.top_walk_anim, start_pos, self.animations)
        self.feature_rotate = "none"

    def process_logic(self):
        if not self.is_invisible:
            super().process_logic()
            self.go()

    def get_love_cell(self, pacman, blinky = None):
        self.love_cell = pacman.get_cell()
