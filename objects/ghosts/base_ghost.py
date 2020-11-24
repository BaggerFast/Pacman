import pygame as pg

from misc.constants import CELL_SIZE
from misc.path import get_image_path_for_animator
from objects.character_base import Character
from misc.animator import Animator


class BaseGhost(Character):
    action = {
        pg.K_UP: 'up',
        pg.K_LEFT: 'left',
        pg.K_DOWN: 'down',
        pg.K_RIGHT: 'right'
    }

    def __init__(self, game, animator: Animator, start_pos: tuple, animations, enable_collision=True, max_count_eat_seeds_in_home=0):
        super().__init__(game, animator, start_pos)
        self.is_can_leave_home = False
        self.animations = animations
        self.enable_collision = enable_collision
        self.count_eat_seeds_in_home = 0
        self.max_count_eat_seeds_in_home = max_count_eat_seeds_in_home
        self.timer = pg.time.get_ticks()
        self.invisible_anim = Animator(
            get_image_path_for_animator('ghost', 'invisible'), is_rotation=False
        )
        self.is_invisible = False
        self.is_in_home = True
        self.work_counter = True
        self.love_cell = (8, 16)

    def process_event(self, event):
        if event.type == pg.KEYDOWN and event.key in self.action.keys():
            self.go()
            self.feature_direction = self.action[event.key]

    def process_logic(self):
        self.animator.timer_check()
        if self.in_center() and self.enable_collision:
            if self.move_to(self.rotate):
                self.go()
            else:
                self.stop()
            direction = {
                0: (1, 0, 0),
                1: (0, 1, 1),
                2: (-1, 0, 2),
                3: (0, -1, 3)
            }
            '''
            direction2 = {
                (1, 0, 0): '',
                (0, 1, 1): '',
                (-1, 0, 2): '',
                (0, -1, 3): ''
            }
            '''
            self.go()
            min_dis = 10000000000000
            cross = self.movement_cell(self.get_cell())
            cross[(self.rotate+2)%4] = 0
            for i in range(4):
                if cross[i]:
                    tmp_cell = (self.get_cell()[0]+direction[i][0], self.get_cell()[1]+direction[i][1])
                    if min_dis > self.two_cells_dis(self.love_cell, tmp_cell):
                        min_dis = self.two_cells_dis(self.love_cell, tmp_cell)
                        self.shift_x, self.shift_y, self.rotate = direction[i]
        if self.rotate is None:
            self.rotate = 0
        self.animator = self.animations[self.rotate]
        if not self.is_invisible:
            self.animator = self.animations[self.rotate]
        super().process_logic()

    def collision_check(self, object: Character):
        return self.get_cell() == object.get_cell() and self.enable_collision

    def counter(self):
        if self.work_counter:
            self.count_eat_seeds_in_home += 1

    def get_cell(self):
        return ((self.rect.centerx) // CELL_SIZE, (self.rect.centery-25) // CELL_SIZE)

    def can_leave_home(self):
        #print(self.max_count_eat_seeds_in_home, ': ', pg.time.get_ticks()-self.timer)
        return (self.count_eat_seeds_in_home >= self.max_count_eat_seeds_in_home and self.work_counter) \
               or pg.time.get_ticks()-self.timer >= 4000 or self.is_can_leave_home
        # флаг выше передаётся нужен после смерти пакмана

    def update_timer(self):
        self.timer = pg.time.get_ticks()

    def invisible(self):
        self.animator = self.invisible_anim
        self.is_invisible = True
        self.enable_collision = False

    def is_cross(self, cell: tuple) -> bool:
        return sum(self.movement_cell(cell)) > 2
