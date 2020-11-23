from misc.animator import Animator
from misc.path import get_image_path_for_animator
from objects.ghosts.base_ghost import BaseGhost


class Clyde(BaseGhost):

    def __init__(self, game, start_pos: tuple, max_count_eat_seeds_in_home=0):
        self.top_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'clyde', 'top'), False
        )
        self.bottom_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'clyde', 'bottom'), False
        )
        self.left_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'clyde', 'left'), False
        )
        self.right_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'clyde', 'right'), False
        )
        self.animations = {
            3: self.top_walk_anim,
            2: self.left_walk_anim,
            1: self.bottom_walk_anim,
            0: self.right_walk_anim
        }
        super().__init__(game, self.top_walk_anim, start_pos, self.animations, False, max_count_eat_seeds_in_home)
        self.feature_rotate = "none"
        self.is_in_home = True

    def process_logic(self):
        super().process_logic()
        if self.is_in_home and self.can_leave_home():
            self.animator = self.right_walk_anim
            self.shift_x = -1
            self.shift_y = 0
            self.speed = 1
            scene = self.game.scenes[self.game.current_scene_index]
            if (self.rect.x == scene.pinky.start_pos[0]):
                self.animator = self.top_walk_anim
                self.shift_x = 0
                self.shift_y = -1
            if (self.rect.y == scene.blinky.start_pos[1]):
                self.shift_x = 1
                self.shift_y = 0
                self.speed = 0
                self.is_in_home = False
                self.enable_collision = True


