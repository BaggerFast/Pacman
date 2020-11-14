from scenes.base import BaseScene as Scene
import pygame as pg
from py.constants import *
import sys
import os


class Character:
    direction = {
        "up": (0, -1),
        "down": (0, 1),
        "right": (1, 0),
        "left": (-1, 0),
        "none": (0, 0)
    }

    def __init__(self, scene: Scene, image: pg.Surface, start_pos: tuple):
        self.scene = scene
        self.image = pg.transform.scale(image, (35, 35))
        self.rect = self.image.get_rect()
        self.shift_x = self.shift_y = 0
        self.change_pos(*start_pos)
        self.speed = 2

    def change_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.x += self.shift_x * self.speed
        self.rect.y += self.shift_y * self.speed

    def set_dir(self, dir="none"):
        self.shift_x, self.shift_y = self.direction[dir]

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

    def draw(self):
        self.scene.screen.blit(self.image, self.rect)


def main():
    pg.init()
    screen_size = width, height = 800, 600
    screen = pg.display.set_mode(screen_size, pg.SCALED)
    exit = True
    char = Character(Scene(screen),
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
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()
    sys.exit()
