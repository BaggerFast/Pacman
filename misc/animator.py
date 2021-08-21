from typing import List
import pygame as pg
from misc.sprite_sheet import SpriteSheet


class Animator:
    def __init__(self, images: List[pg.Surface], time_out: int = 50, repeat: bool = True,
                 aura: str = None):
        self.__time_out = time_out
        self.__animate_timer = 0
        self.images: List[pg.Surface] = images
        self.current_index: int = 0
        self.current_aura = pg.image.load(aura) if aura else aura
        self.__repeat: bool = repeat
        self.anim_finished: bool = False
        self.__run: bool = False

    @property
    def current_image(self) -> pg.Surface:
        return self.images[self.current_index]

    def get_len_anim(self) -> int:
        return len(self.images)

    def stop(self) -> None:
        self.__run = False

    def start(self) -> None:
        self.__run = True

    def timer_check(self) -> None:
        if pg.time.get_ticks() - self.__animate_timer > self.__time_out and self.__run:
            self.__animate_timer = pg.time.get_ticks()
            self.current_index += 1
            self.image_swap()

    def change_cur_image(self, index: int) -> None:
        self.current_index = index

    def change_cur_aura(self, aura: str = None) -> None:
        self.current_aura = pg.image.load(aura) if aura else aura

    def image_swap(self) -> None:
        if self.current_index == len(self.images)-1:
            if not self.__repeat:
                self.stop()
                self.anim_finished = True
                return
        self.current_index %= len(self.images)


class SpriteSheetAnimator(Animator):
    def __init__(self, sheet: SpriteSheet, time_out: int = 50, repeat: bool = True, aura: str = None):
        self.sheet: SpriteSheet = sheet
        self.rotate: int = 0
        super().__init__(self.sheet[0], time_out, repeat, aura)

    @property
    def current_image(self) -> pg.Surface:
        return self.sheet[self.rotate % len(self.sheet)][self.current_index]
