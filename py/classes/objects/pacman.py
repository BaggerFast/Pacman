from py.classes.objects.character_base import Character
from scenes.base import BaseScene as Scene
import pygame as pg
from py.constants import *
import sys
import os


class Pacman(Character):
    def __init__(self, scene: Scene, image: pg.Surface, start_pos: tuple):
        super().__init__(scene, image, start_pos)

    def check_event(self, event):
        keys = pg.key.get_pressed()
        check_sum = keys[pg.K_a] + keys[pg.K_d] + keys[pg.K_s] + keys[pg.K_w]
        if check_sum > 1 or check_sum < 1:
            self.set_dir()
        else:
            if keys[pg.K_a]:
                self.set_dir("left")
            if keys[pg.K_d]:
                self.set_dir("right")
            if keys[pg.K_w]:
                self.set_dir("up")
            if keys[pg.K_s]:
                self.set_dir("down")


def main():
    pg.init()
    screen_size = width, height = 800, 600
    screen = pg.display.set_mode(screen_size, pg.SCALED)
    exit = True
    char = Pacman(Scene(screen),
                     pg.image.load(os.path.join("images", "pacman.png")),
                     (10, 10))
    while exit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit = False
            char.check_event(event)

        char.move()
        screen.fill(Color.BLACK)

        char.draw()
        pg.display.flip()
        pg.time.wait(10)


if __name__ == '__main__':
    main()
    sys.exit()
