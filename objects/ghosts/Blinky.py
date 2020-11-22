from misc.animator import Animator
from misc.path import get_image_path_for_animator
from objects.ghosts.base_ghost import BaseGhost


class Blinky(BaseGhost):

    def __init__(self, game, start_pos: tuple):
        self.top_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'blinky', 'top'), False
        )
        self.bottom_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'blinky', 'bottom'), False
        )
        self.left_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'blinky', 'left'), False
        )
        self.right_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'blinky', 'right'), False
        )
        self.animations = {
            3: self.top_walk_anim,
            2: self.left_walk_anim,
            1: self.bottom_walk_anim,
            0: self.right_walk_anim
        }


        super().__init__(game, self.top_walk_anim, start_pos, self.animations)
        self.feature_rotate = "none"


