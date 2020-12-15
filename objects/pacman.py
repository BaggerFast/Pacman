import pygame as pg
from misc.path import get_path
from objects.character_base import Character

from typing import Tuple


class Pacman(Character):
    action = {
        pg.K_w: 'up',
        pg.K_a: 'left',
        pg.K_s: 'down',
        pg.K_d: 'right'
    }

    def __init__(self, game, start_pos: Tuple[int, int]) -> None:
        self.__walk_anim = game.skins.current.walk
        self.__dead_anim = game.skins.current.dead
        super().__init__(game, self.__walk_anim, start_pos, get_path('aura', 'png', 'images', 'pacman', game.skins.current.name))
        self.dead = False
        self.__feature_rotate = "none"

    @property
    def dead_anim(self):
        return self.__dead_anim

    def process_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key in self.action.keys() and not self.dead:
            self.go()
            self.__feature_rotate = self.action[event.key]

    def process_logic(self) -> None:
        self.animator.timer_check()
        if not self.dead:
            if self.in_center():
                if self.move_to(self.rotate):
                    self.go()
                else:
                    self.stop()
                    self.animator.change_cur_image(0)
                c = self.direction[self.__feature_rotate][2]
                if self.move_to(c):
                    self.set_direction(self.__feature_rotate)
            super().process_logic()

    def death(self) -> None:
        if not self.game.cheats_var.INFINITY_LIVES:
            self.game.current_scene.hp -= 1
        self.animator = self.__dead_anim
        self.game.sounds.siren.pause()
        self.game.sounds.pellet.stop()
        self.game.sounds.pacman.play()
        self.animator.start()
        self.dead = True
