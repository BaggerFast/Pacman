import pygame as pg
from misc import Sounds
from misc.path import get_list_path
from objects.character_base import Character
from misc.health import Health
from misc.animator import Animator
from typing import Tuple


class Pacman(Character):
    action = {
        pg.K_w: 'up',
        pg.K_a: 'left',
        pg.K_s: 'down',
        pg.K_d: 'right'
    }

    pg.mixer.init()
    death_sound = Sounds.DEAD

    def __init__(self, game, start_pos: Tuple[int, int]) -> None:
        self.__walk_anim = Animator(
            get_list_path('png', 'images', 'pacman', 'walk')
        )
        self.__dead_anim = Animator(
            get_list_path('png', 'images', 'pacman', 'dead'), 100, False, True
        )
        super().__init__(game, self.__walk_anim, start_pos)
        self.dead = False
        self.__feature_rotate = "none"
        pg.mixer.Channel(3).unpause()

    @property
    def hp(self):
        return self.__hp.lives

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
        pg.mixer.Channel(3).pause()
        pg.mixer.Channel(0).play(self.death_sound)
        self.game.current_scene.hp -= 1
        self.animator = self.__dead_anim
        self.animator.start()
        self.dead = True
