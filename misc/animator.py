import pygame as pg


class Animator:
    TIMEOUT = 150

    def __init__(self, path_to_images, is_rotation=True):
        self.is_rotation = is_rotation
        self.animate_timer = 0
        self.images = self.add_image(path_to_images)
        self.current_image_index = 0
        self.current_image = self.images[self.current_image_index]
        self.rotate = 0
        self.run = False

    def add_image(self, path_to_images):
        images = []
        for i in range(len(path_to_images)):
            images.append(pg.image.load(path_to_images[i]))
        return images

    def stop(self):
        self.run = False

    def start(self):
        self.run = True

    def timer_check(self):
        if pg.time.get_ticks() - self.animate_timer > self.TIMEOUT and self.run:
            self.animate_timer = pg.time.get_ticks()
            self.current_image_index += 1
            self.image_swap()

    def image_swap(self):
        if self.current_image_index == len(self.images):
            self.current_image_index = 0
        self.current_image = self.images[self.current_image_index]
        if self.is_rotation:
            self.change_rotation()

    def change_rotation(self):
        self.current_image = pg.transform.rotate(self.images[self.current_image_index], -90 * self.rotate)
