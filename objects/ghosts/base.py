import pygame as pg
from misc import Animator, get_list_path, DISABLE_GHOSTS_MOVING, DISABLE_GHOSTS_COLLISION
from objects import Character
from typing import Tuple
import random


class Base(Character):
    love_point_in_scatter_mode = (0, 0)
    max_count_eat_seeds_in_home = 0
    direction2 = {
        0: (1, 0, 0),
        1: (0, 1, 1),
        2: (-1, 0, 2),
        3: (0, -1, 3)
    }

    def __init__(self, game, start_pos: Tuple[int, int]) -> None:

        self.process_logic_iterator = 0
        self.deceleration_multiplier = 1

        # Обычные Анимация
        self.left_walk_anim = Animator(
            get_list_path('png', 'images', 'ghost', type(self).__name__.lower(), 'left'), is_rotation=False
        )
        self.right_walk_anim = Animator(
            get_list_path('png', 'images', 'ghost', type(self).__name__.lower(), 'right'), is_rotation=False
        )
        self.top_walk_anim = Animator(
            get_list_path('png', 'images', 'ghost', type(self).__name__.lower(), 'top'), is_rotation=False
        )
        self.bottom_walk_anim = Animator(
            get_list_path('png', 'images', 'ghost', type(self).__name__.lower(), 'bottom'), is_rotation=False
        )

        # Анимации страха

        self.frightened_walk_anim1 = Animator(
            get_list_path('png', 'images', 'ghost', 'fear1'), is_rotation=False
        )

        self.frightened_walk_anim2 = Animator(
            get_list_path('png', 'images', 'ghost', 'fear2'), is_rotation=False
        )

        self.animations = [
            self.right_walk_anim,
            self.bottom_walk_anim,
            self.left_walk_anim,
            self.top_walk_anim,
        ]

        super().__init__(game, self.top_walk_anim, start_pos)

        self.is_can_leave_home = False
        self.collision = False
        self.count_eat_seeds_in_home = 0
        self.timer = pg.time.get_ticks()
        self.ai_timer = pg.time.get_ticks()
        self.invisible_anim = Animator(
            get_list_path('png', 'images', 'ghost', 'invisible'), is_rotation=False
        )
        self.love_cell = (0, 0)
        self.is_invisible = False
        self.is_in_home = True
        self.work_counter = True
        self.set_direction("left")
        '''
            'Chase',
            'Scatter',
            'Frightened'
        '''
        self.mode = 'Scatter'
    def process_logic(self) -> None:
        if self.rotate is None:
            self.rotate = 0
        if not self.is_invisible and self.mode != 'Frightened':
            self.animator = self.animations[self.rotate]
        if not self.process_logic_iterator % self.deceleration_multiplier:
            self.ghosts_ai()
            self.step()
        self.process_logic_iterator += 1

    def collision_check(self, object: Character):
        return (self.two_cells_dis(self.rect.center, object.rect.center) < 4 and self.collision and not DISABLE_GHOSTS_COLLISION,
                self.mode != 'Frightened')

    def counter(self) -> None:
        if self.work_counter:
            self.count_eat_seeds_in_home += 1

    def can_leave_home(self) -> bool:
        return (self.count_eat_seeds_in_home >= self.max_count_eat_seeds_in_home and self.work_counter) \
               or pg.time.get_ticks()-self.timer >= 4000 or self.is_can_leave_home

    def update_timer(self) -> None:
        self.timer = pg.time.get_ticks()

    def invisible(self) -> None:
        self.animator = self.invisible_anim
        self.is_invisible = True
        self.collision = False

    def update_ai_timer(self):
        self.ai_timer = pg.time.get_ticks()

    def ghosts_ai(self) -> None:
        self.animator.timer_check()
        if self.in_center() and self.collision:
            if self.move_to(self.rotate):
                self.go()
            cell = self.movement_cell(self.get_cell())
            cell[(self.rotate + 2) % 4] = False
            '''
            rotate

            0:
            1:
            2:
            3:
            '''
            if self.mode != 'Frightened':
                min_dis = 10000000000000
                for i in range(4):
                    if cell[i]:
                        tmp_cell = (self.get_cell()[0] + self.direction2[i][0], self.get_cell()[1] + self.direction2[i][1])
                        if min_dis > self.two_cells_dis(self.love_cell, tmp_cell):
                            min_dis = self.two_cells_dis(self.love_cell, tmp_cell)
                            self.shift_x, self.shift_y, self.rotate = self.direction2[i]
            else:
                while True:
                    rand = random.randrange(4)
                    if cell[rand]:
                        break
                self.shift_x, self.shift_y, self.rotate = self.direction2[rand]
                if pg.time.get_ticks() - self.ai_timer >= 6000:
                    self.animator = self.frightened_walk_anim2
                if pg.time.get_ticks() - self.ai_timer >= 8000:
                    self.update_ai_timer()
                    self.deceleration_multiplier = 1
                    self.mode = 'Scatter'
    def step(self) -> None:
        if not DISABLE_GHOSTS_MOVING:
            super().step()

    def toggle_mode_to_frightened(self):
        self.update_ai_timer()
        self.mode = 'Frightened'
        self.animator = self.frightened_walk_anim1
        self.deceleration_multiplier = 2

    def toggle_mode_to_eye(self):
        pass
