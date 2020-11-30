import pygame as pg
from misc import Animator, get_image_path_for_animator
from objects import Character
from objects.pacman import Pacman
from typing import Tuple


class Base(Character):
    max_count_eat_seeds_in_home = 0
    direction2 = {
        0: (1, 0, 0),
        1: (0, 1, 1),
        2: (-1, 0, 2),
        3: (0, -1, 3)
    }

    def __init__(self, game, start_pos: Tuple[int, int]) -> None:

        self.left_walk_anim = Animator(
            get_image_path_for_animator('ghost', type(self).__name__.lower(), 'left'), is_rotation=False
        )
        self.right_walk_anim = Animator(
            get_image_path_for_animator('ghost', type(self).__name__.lower(), 'right'), is_rotation=False
        )
        self.top_walk_anim = Animator(
            get_image_path_for_animator('ghost', type(self).__name__.lower(), 'top'), is_rotation=False
        )
        self.bottom_walk_anim = Animator(
            get_image_path_for_animator('ghost', type(self).__name__.lower(), 'bottom'), is_rotation=False
        )

        self.animations = [
            self.right_walk_anim,
            self.bottom_walk_anim,
            self.left_walk_anim,
            self.top_walk_anim,
        ]

        super().__init__(game, self.right_walk_anim, start_pos)

        self.is_can_leave_home = False
        self.collision = False
        self.count_eat_seeds_in_home = 0
        self.timer = pg.time.get_ticks()
        self.ai_timer = pg.time.get_ticks()
        self.invisible_anim = Animator(
            get_image_path_for_animator('ghost', 'invisible'), is_rotation=False
        )
        self.is_invisible = False
        self.is_in_home = True
        self.work_counter = True
        self.love_cell = (8, 16)
        self.set_direction("left")
        self.love_point_in_runaway_mode = (0,0)
        '''
            'Chase',
            'Scatter',
            'Frightened'
        '''
        self.mode = 'Scatter'
    def process_logic(self) -> None:
        self.animator.timer_check()
        if self.in_center() and self.collision:
            if self.move_to(self.rotate):
                self.go()
            else:
                self.stop()
            min_dis = 10000000000000
            cell = self.movement_cell(self.get_cell())
            cell[(self.rotate + 2) % 4] = 0
            for i in range(4):
                if cell[i]:
                    tmp_cell = (self.get_cell()[0]+self.direction2[i][0], self.get_cell()[1]+self.direction2[i][1])
                    if min_dis > self.two_cells_dis(self.love_cell, tmp_cell):
                        min_dis = self.two_cells_dis(self.love_cell, tmp_cell)
                        self.shift_x, self.shift_y, self.rotate = self.direction2[i]
        if self.rotate is None:
            self.rotate = 0
        self.animator = self.animations[self.rotate]
        if not self.is_invisible:
            self.animator = self.animations[self.rotate]
        super().process_logic()

    def collision_check(self, object: Character):
        return self.get_cell() == object.get_cell() and self.collision

    def counter(self) -> None:
        if self.work_counter:
            self.count_eat_seeds_in_home += 1

    def can_leave_home(self) -> bool:
        # print(type(self).__name__, ' ', self.count_eat_seeds_in_home >= self.max_count_eat_seeds_in_home, pg.time.get_ticks()-self.timer)
        return (self.count_eat_seeds_in_home >= self.max_count_eat_seeds_in_home and self.work_counter) \
               or pg.time.get_ticks()-self.timer >= 4000 or self.is_can_leave_home

    def update_timer(self) -> None:
        self.timer = pg.time.get_ticks()

    def invisible(self) -> None:
        self.animator = self.invisible_anim
        self.is_invisible = True
        self.collision = False

    def get_love_cell(self, pacman: Pacman) -> None:
        if self.mode == 'Scater':
            self.love_cell = self.love_point_in_runaway_mode
