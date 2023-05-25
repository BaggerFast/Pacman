import pygame as pg

from pacman.data_core import EvenType, IEventful
from pacman.misc import CellUtil
from pacman.storage import SkinStorage

from .character_base import Character


class Pacman(Character, IEventful):
    action = {EvenType.UP_BTN: "up", EvenType.LEFT_BTN: "left", EvenType.DONW_BTN: "down", EvenType.RIGHT_BTN: "right"}

    def __init__(self, loader) -> None:
        skin_instanse = SkinStorage().current_instance
        self.__walk_anim = skin_instanse.walk
        self.__dead_anim = skin_instanse.dead
        super().__init__(self.__walk_anim, loader, f"pacman/{skin_instanse.name}/aura")
        self.is_dead = False
        self.__feature_rotate = "none"
        self.__ai_timer = 0
        self.animator.stop()

    @property
    def dead_anim(self):
        return self.__dead_anim

    def event_handler(self, event: pg.event.Event) -> None:
        if event.type in self.action and not self.is_dead:
            self.go()
            self.__feature_rotate = self.action[event.type]

    def update(self) -> None:
        self.animator.update()
        if not self.is_dead:
            if CellUtil.is_in_cell_center(self.rect):
                if self.can_rotate_to(self.rotate):
                    self.go()
                else:
                    self.stop()
                    self.animator.set_cur_image(0)
                c = self.direction[self.__feature_rotate][2]
                if self.can_rotate_to(c):
                    self.set_direction(self.__feature_rotate)
            super().update()

    def death(self) -> None:
        self.__ai_timer = pg.time.get_ticks()
        self.animator = self.__dead_anim
        self.animator.start()
        self.is_dead = True

    def death_is_finished(self) -> bool:
        return pg.time.get_ticks() - self.__ai_timer >= 2500 and self.animator.is_finished and self.is_dead
