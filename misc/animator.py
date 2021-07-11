import pygame as pg
from typing import List


class Animator:
    __time_out = 50

    def __init__(self, path_to_images: List[str], time_out: int = 50, is_rotation: bool = True, repeat: bool = False,
                 aura: str = None):
        self.is_rotation = is_rotation
        self.__animate_timer = 0
        self.__time_out = time_out
        self.__images: List[pg.Surface] = self.__add_image(path_to_images)
        self.__current_image_index: int = 0
        self.__current_image = self.__images[self.__current_image_index]
        self.__current_aura = pg.image.load(aura) if aura else aura
        self.rotate: int = 0
        self.__repeat: bool = repeat
        self.anim_finished: bool = False
        self.run: bool = False

    @property
    def current_image(self):
        return self.__current_image

    @property
    def current_aura(self):
        return self.__current_aura

    def __add_image(self, path_to_images: List[str]) -> List[pg.Surface]:
        return [pg.image.load(path_image) for path_image in path_to_images]

    def get_len_anim(self) -> int:
        return len(self.__images)

    def get_cur_index(self) -> int:
        return self.__current_image_index

    def stop(self) -> None:
        self.run = False

    def start(self) -> None:
        self.run = True

    def timer_check(self) -> None:
        if pg.time.get_ticks() - self.__animate_timer > self.__time_out and self.run:
            self.__animate_timer = pg.time.get_ticks()
            self.__current_image_index += 1
            self.__image_swap()

    def change_cur_image(self, index: int) -> None:
        self.__current_image_index = index
        self.__current_image = self.__images[self.__current_image_index]

    def change_cur_aura(self, aura: str = None) -> None:
        self.__current_aura = pg.image.load(aura) if aura else aura

    def __image_swap(self) -> None:
        if self.__current_image_index == len(self.__images):
            self.__current_image_index = 0
            if self.__repeat:
                self.stop()
                self.anim_finished = True
                return
        self.__current_image = self.__images[self.__current_image_index]
        if self.is_rotation:
            self.change_rotation()

    def change_rotation(self) -> None:
        right = 2
        if self.rotate == right:
            self.mirror_x()
            return
        self.__current_image = pg.transform.rotate(self.current_image, -90 * self.rotate)

    def mirror_x(self) -> None:
        self.__current_image = pg.transform.flip(self.current_image, True, False)
