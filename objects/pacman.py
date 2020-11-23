import pygame as pg
from misc.constants import CELL_SIZE
from misc.path import get_image_path_for_animator
from objects.character_base import Character
from misc.health import Health
from misc.animator import Animator


class Pacman(Character):
    action = {
        pg.K_w: 'up',
        pg.K_a: 'left',
        pg.K_s: 'down',
        pg.K_d: 'right'
    }

    def __init__(self, game, start_pos: tuple):
        self.hp = Health(3, 3)
        self.walk_anim = Animator(
            get_image_path_for_animator('pacman', 'walk')
        )
        self.dead_anim = Animator(
            get_image_path_for_animator('pacman', 'dead'), 100, False, True
        )
        super().__init__(game, self.walk_anim, start_pos)
        self.dead = False
        self.feature_rotate = "none"

    def process_event(self, event):
        if event.type == pg.KEYDOWN and event.key in self.action.keys() and not self.dead:
            self.go()
            self.feature_rotate = self.action[event.key]

    def process_logic(self):
        self.animator.timer_check()
        if not self.dead:
            if self.in_center():
                if self.move_to(self.rotate):
                    self.go()
                else:
                    self.stop()
                c = self.direction[self.feature_rotate][2]
                if self.move_to(c):
                    self.set_direction(self.feature_rotate)
            super().process_logic()

    def movement_cell(self):
        scene = self.game.scenes_dict[self.game.current_scene_name]
        cell = scene.movements_data[(self.rect.y-12) // CELL_SIZE][self.rect.x // CELL_SIZE+1]
        return "{0:04b}".format(cell)[::-1]

    def move_to(self, direction):
        return self.movement_cell()[direction] == "1"

    def death(self):
        self.hp.change_count_lives(-1)
        if not int(self.hp):
            self.animator = self.dead_anim
            self.animator.run = True
            self.dead = True
        else:
            self.move(*self.start_pos)
            self.speed = 0
            self.shift_x, self.shift_y = self.direction["right"][:2]
            self.animator.stop()
            self.animator.change_cur_image(0)

    def in_center(self) -> bool:
        return self.rect.x % CELL_SIZE == 6 and (self.rect.y-20) % CELL_SIZE == 6
