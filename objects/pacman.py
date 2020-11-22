import pygame as pg

from misc.path import get_image_path_for_animator
from objects.character_base import Character
from misc.animator import Animator


class Pacman(Character):
    action = {
        pg.K_w: 'up',
        pg.K_a: 'left',
        pg.K_s: 'down',
        pg.K_d: 'right'
    }

    def __init__(self, game, start_pos: tuple):
        self.walk_anim = Animator(
            get_image_path_for_animator('Pacman', 'walk')
        )
        self.current_anim = self.walk_anim
        super().__init__(game, self.current_anim, start_pos)
        self.feature_rotate = "none"

    def process_event(self, event):
        if event.type == pg.KEYDOWN and event.key in self.action.keys():
            self.go()
            self.feature_rotate = self.action[event.key]

    def process_logic(self):
        self.animator.timer_check()
        if self.in_center():
            if self.move_to(self.rotate):
                self.go()
            else:
                self.stop()
            c = self.direction[self.feature_rotate][2]
            if self.move_to(c):
                self.set_direction(self.feature_rotate)
        super().process_logic()
