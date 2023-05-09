import pygame as pg


class Animator:
    def __init__(self, images: list[pg.Surface], time_out: int = 125, repeat: bool = True):
        self.__time_out = time_out
        self.__animate_timer = 0
        self.__repeat = repeat
        self.__run = True
        self.images = images
        self.current_index: int = 0
        self.__anim_finished: bool = False

    @property
    def anim_finished(self) -> bool:
        return self.__anim_finished

    @property
    def current_image(self) -> pg.Surface:
        return self.images[self.current_index]

    def stop(self) -> None:
        self.__run = False

    def start(self) -> None:
        self.__run = True

    def update(self) -> None:
        if pg.time.get_ticks() - self.__animate_timer > self.__time_out and self.__run:
            self.__animate_timer = pg.time.get_ticks()
            self.current_index += 1
            self.image_swap()

    def change_cur_image(self, index: int) -> None:
        self.current_index = index

    def image_swap(self) -> None:
        if self.current_index == len(self.images) - 1 and not self.__repeat:
            self.stop()
            self.__anim_finished = True
            return
        self.current_index %= len(self.images)

    def reset(self):
        self.current_index = 0
