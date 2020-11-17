import pygame as pg


class Animator:
    def __init__(self, *path_to_images):
        self.animate_timer = 0
        self.images = self.add_image(path_to_images)
        self.index_image = 0
        self.current_image = self.images[self.index_image]
        self.rotate = 0

    def add_image(self, path_to_images):
        images = []
        for i in range(len(path_to_images)):
            images.append(pg.image.load(path_to_images[i]))
        return images

    def timer_check(self):
        if pg.time.get_ticks() - self.animate_timer > 500:
            self.animate_timer = pg.time.get_ticks()
            self.index_image += 1
            self.image_swap()

    def image_swap(self):
        if self.index_image == len(self.images):
            self.index_image = 0
        self.current_image = self.images[self.index_image]
        self.change_rotation()

    def change_rotation(self):
        self.current_image = pg.transform.rotate(self.images[self.index_image], -90*self.rotate)


if __name__ == "__main__":
    pg.init()
    screen_size = width, height = 224, 248
    screen = pg.display.set_mode(screen_size, pg.SCALED)
    a = Animator("images/Pacman1.png", 'images/Pacman2.png')
    exit = True
    while exit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit = False
        a.timer_check()
        screen.fill((0, 0, 0))
        screen.blit(a.current_image, (100,100))
        pg.display.flip()
        pg.time.wait(10)
