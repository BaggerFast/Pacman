import pygame as pg
from misc import CELL_SIZE, Color
from objects import DrawableObject

from misc import CELL_SIZE, Color
from objects import DrawableObject


class SeedContainer(DrawableObject):
    def __init__(self, game, seed_data, energizer_data, x=0, y=20):
        super().__init__(game)
        self.x = x
        self.y = y
        self.seeds = seed_data
        self.energizers = energizer_data
        self.anim = 0

        self.time_out = 125
        self.animate_timer = 0
        self.color = {
            -1: Color.WHITE,
            1: Color.BLACK
        }
        self.index_color = 1

    def draw_seeds(self):
        for row in range(len(self.seeds)):
            for col in range(len(self.seeds[row])):
                if self.seeds[row][col]:
                    pg.draw.circle(self.game.screen, Color.WHITE, (self.x + col * CELL_SIZE + CELL_SIZE//2,

                                                                           self.y + row * CELL_SIZE + CELL_SIZE//2), 1)
    def draw_energizers(self):
        if pg.time.get_ticks() - self.animate_timer > self.time_out:
            self.animate_timer = pg.time.get_ticks()
            self.index_color *= -1
        for energizer in self.energizers:
            pg.draw.circle(self.game.screen, self.color[self.index_color], (self.x + energizer[0] * CELL_SIZE + CELL_SIZE//2,
                                                                   self.y + energizer[1] * CELL_SIZE + CELL_SIZE//2), 4)

    def process_draw(self):
        self.draw_seeds()
        self.draw_energizers()

    def process_collision(self, object): #for pacman only
        for row in range(len(self.seeds)):
            for col in range(len(self.seeds[row])):
                if self.seeds[row][col] and row * CELL_SIZE + 18 == object.rect.y:
                    if col * CELL_SIZE - 2 == object.rect.x:
                        self.seeds[row][col] = None
                        return True, "seed"
        for energizer in self.energizers:
            if energizer[1] * CELL_SIZE + 18 == object.rect.y:
                if energizer[0] * CELL_SIZE - 2 == object.rect.x:
                    self.energizers.remove(energizer)
                    return True, "energizer"
        return False, ""
