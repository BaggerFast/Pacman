from misc import Animator, CELL_SIZE, get_image_path_for_animator
from .base import Base


class Pinky(Base):

    def __init__(self, game, start_pos: tuple, max_count_eat_seeds_in_home=0):
        self.ghost_positions = None
        self.top_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'pinky', 'top'),  is_rotation=False
        )
        self.bottom_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'pinky', 'bottom'),  is_rotation=False
        )
        self.left_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'pinky', 'left'),  is_rotation=False
        )
        self.right_walk_anim = Animator(
            get_image_path_for_animator('ghost', 'pinky', 'right'),  is_rotation=False
        )
        self.animations = {
            3: self.top_walk_anim,
            2: self.left_walk_anim,
            1: self.bottom_walk_anim,
            0: self.right_walk_anim
        }
        super().__init__(game, self.top_walk_anim, start_pos, self.animations, False, max_count_eat_seeds_in_home)
        self.feature_rotate = "none"

    def process_logic(self):
        if not self.is_invisible:
            super().process_logic()
            if self.is_in_home and self.can_leave_home():
                self.animator = self.top_walk_anim
                self.shift_x = 0
                self.shift_y = -1
                self.speed = 1
                scene = self.game.scenes[self.game.current_scene_name]
                if (self.rect.y == scene.blinky.start_pos[1]):
                    self.shift_x = 1
                    self.shift_y = 0
                    self.is_in_home = False
                    self.enable_collision = True

    def get_love_cell(self, pacman, blinky = None):
        rotate = pacman.rotate
        self.love_cell = (pacman.get_cell()[0]+self.direction2[rotate][0]*2, pacman.get_cell()[1]+self.direction2[rotate][1]*2)

'''
direction = {
        "right": (1, 0, 0),
        "down": (0, 1, 1),
        "left": (-1, 0, 2),
        "up": (0, -1, 3),
        "none": (0, 0, None)
    }
'''
