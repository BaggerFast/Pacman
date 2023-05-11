from typing import Tuple
import pygame as pg
from pacman.data_core import PathManager
from pacman.data_core.interfaces import IEventful
from pacman.misc.cell_util import CellUtil
from pacman.objects.character_base import Character


class Pacman(Character, IEventful):
    action = {pg.K_w: "up", pg.K_a: "left", pg.K_s: "down", pg.K_d: "right"}

    def __init__(self, game, loader) -> None:
        self.__walk_anim = game.skins.current.walk
        self.__dead_anim = game.skins.current.dead
        super().__init__(
            game, self.__walk_anim, loader, PathManager.get_image_path(f"pacman/{game.skins.current.name}/aura")
        )
        self.is_dead = False
        self.__feature_rotate = "none"
        self.timer_reset = 0

    @property
    def dead_anim(self):
        return self.__dead_anim

    def event_handler(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key in self.action.keys() and not self.is_dead:
            self.go()
            self.__feature_rotate = self.action[event.key]

    def update(self) -> None:
        self.animator.timer_check()
        if not self.is_dead:
            if CellUtil.in_cell_center(self.rect):
                if self.can_rotate_to(self.rotate):
                    self.go()
                else:
                    self.stop()
                    self.animator.change_cur_image(0)
                c = self.direction[self.__feature_rotate][2]
                if self.can_rotate_to(c):
                    self.set_direction(self.__feature_rotate)
            super().update()

    def death(self) -> None:
        self.timer_reset = pg.time.get_ticks()
        self.animator = self.__dead_anim
        self.game.sounds.siren.pause()
        self.game.sounds.pellet.stop()
        self.game.sounds.pacman.play()
        self.animator.start()
        self.is_dead = True

    def death_is_finished(self) -> bool:
        return pg.time.get_ticks() - self.timer_reset >= 3000 and self.animator.anim_finished and self.is_dead
