import sys

import pygame as pg

from py.classes.objects.character_base import Character
from py.constants import *
from scenes.base import BaseScene as Scene
from py.classes.objects.animator import Animator


class Pacman(Character):
    def __init__(self, scene: Scene, start_pos: tuple):
        self.a = Animator("images/Pacman1.png", 'images/Pacman2.png')
        super().__init__(scene, self.a, start_pos)

    def check_event(self):
        keys = pg.key.get_pressed()
        check_sum = keys[pg.K_a] + keys[pg.K_d] + keys[pg.K_s] + keys[pg.K_w]
        if check_sum == 0:
            pass
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
    screen_size = width, height = 224, 248
    screen = pg.display.set_mode(screen_size, pg.SCALED)
    exit = True
    char = Pacman(Scene(screen), (10, 10))
    while exit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit = False
            char.check_event()
        char.a.timer_check()
        char.move()
        screen.fill(Color.BLACK)

        char.draw()
        pg.display.flip()
        pg.time.wait(10)


if __name__ == '__main__':
    main()
    sys.exit()
