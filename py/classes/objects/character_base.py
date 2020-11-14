from scenes.base import BaseScene as Scene
import pygame as pg
from py.constants import *


class Character:
    def __init__(self, scene: Scene, image: pg.Surface, start_pos: tuple):
        self.image = image
        self.rect = self.image.get_rect()
        self.shift_x = self.shift_y = 0
        self.change_pos(*start_pos)
        self.scene = scene
        self.speed = 2

    def change_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.x += self.shift_x * self.speed
        self.rect.y += self.shift_y * self.speed

    def check_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                self.shift_x = 1
            if event.key == pg.K_a:
                self.shift_x = -1
            if event.key == pg.K_w:
                self.shift_y = -1
            if event.key == pg.K_s:
                self.shift_y = 1
        if event.type == pg.KEYUP:
            if event.key == pg.K_d:
                self.shift_x = 0
            if event.key == pg.K_a:
                self.shift_x = 0
            if event.key == pg.K_w:
                self.shift_y = 0
            if event.key == pg.K_s:
                self.shift_y = 0

    def draw(self):
        self.scene.screen.blit(self.image, self.rect)


def main():
    pg.init()
    screen_size = width, height = 800, 600
    screen = pg.display.set_mode(screen_size, pg.SCALED)

    char = Character(Scene(screen),
                     pg.image.load(
                         "E:/MyCodes/Py/EduApp/pacman/py/classes/objects"
                         "/intranet.png"),
                     (10, 10))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            char.check_event(event)

        char.move()
        screen.fill(Color.BLACK)

        char.draw()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()
