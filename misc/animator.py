import pygame as pg


class Animator:
    __time_out = 50

    def __init__(self, path_to_images: list, time_out: int = 50, is_rotation: bool = True, repeat: bool = False, aura: str = None):
        self.is_rotation = is_rotation
        self.__animate_timer = 0
        self.__time_out = time_out
        self.__add_image(path_to_images)
        self.__current_image_index = 0
        self.__current_image = self.__images[self.__current_image_index]
        self.__current_aura = pg.image.load(aura) if aura else aura
        self.rotate = 0
        self.__repeat = repeat
        self.anim_finished = False
        self.run = False

    @property
    def current_image(self):
        return self.__current_image

    @property
    def current_aura(self):
        return self.__current_aura

    @property
    def current_path(self):
        return self.__pathes[self.__current_image_index]

    def __add_image(self, path_to_images: list) -> None:
        self.__pathes = []
        self.__images = []
        for i in range(len(path_to_images)):
            self.__pathes.append(path_to_images[i])
            self.__images.append(pg.image.load(path_to_images[i]))

    def recolor(self, game):
        if game:
            for i in range(len(self.__images)):
                for x in range(self.__images[i].get_width()):
                    for y in range(self.__images[i].get_height()):
                        if self.__images[i].get_at((x, y)) == (255, 255, 0):
                            self.__images[i].set_at((x, y), game.pacman_color)  # Set the color of the pixel.

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
                self.change_cur_image(len(self.__images) - 1)
                self.anim_finished = True
        self.__current_image = self.__images[self.__current_image_index]
        if self.is_rotation:
            self.change_rotation()

    def change_rotation(self) -> None:
        if self.rotate == 2:
            self.mirror_x()
        else:
            self.__current_image = pg.transform.rotate(self.current_image, -90 * self.rotate)

    def mirror_x(self) -> None:
        self.__current_image = pg.transform.flip(self.current_image, True, False)
