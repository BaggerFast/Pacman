import pygame as pg
from objects import DrawableObject
from misc.constants import CELL_SIZE, Color


class SeedContainer(DrawableObject):
    def __init__(self, game, seed_data, energizer_data, x=0, y=20):
        super().__init__(game)
        self.__x = x
        self.__y = y
        self.__seeds = seed_data
        self.__energizers = energizer_data
        self.__time_out = 125
        self.__animate_timer = 0
        self.__color = {
            -1: Color.WHITE,
            1: Color.BLACK
        }
        self.__index_color = 1

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __draw_seeds(self):
        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if self.__seeds[row][col]:
                    pg.draw.circle(self.game.screen, Color.WHITE, (self.__x + col * CELL_SIZE + CELL_SIZE // 2,
                                                                   self.y + row * CELL_SIZE + CELL_SIZE//2), 1)

    def __draw_energizers(self):
        if pg.time.get_ticks() - self.__animate_timer > self.__time_out:
            self.__animate_timer = pg.time.get_ticks()
            self.__index_color *= -1
        for energizer in self.__energizers:
            pg.draw.circle(self.game.screen, self.__color[self.__index_color],
                           (self.x + energizer[0] * CELL_SIZE + CELL_SIZE // 2,
                            self.y + energizer[1] * CELL_SIZE + CELL_SIZE // 2), 4)

    def process_draw(self):
        self.__draw_seeds()
        self.__draw_energizers()

    def process_collision(self, object):
        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if self.__seeds[row][col] and row * CELL_SIZE + 18 == object.rect.y:
                    if col * CELL_SIZE - 2 == object.rect.x:
                        self.__seeds[row][col] = None
                        return True, "seed"
        for energizer in self.__energizers:
            if energizer[1] * CELL_SIZE + 18 == object.rect.y:
                if energizer[0] * CELL_SIZE - 2 == object.rect.x:
                    self.__energizers.remove(energizer)
                    return True, "energizer"
        return False, ""
