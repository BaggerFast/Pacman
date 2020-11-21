import pygame as pg

from objects.base import DrawableObject
from misc.constants import CELL_SIZE

def main():
    pass


if __name__ == '__main__':
    main()


class SeedContainer(DrawableObject):
    def __init__(self, game, seed_data, energizer_data, x=0, y=20):
        super().__init__(game)
        self.x = x
        self.y = y
        self.seeds = seed_data
        self.energizers = energizer_data

    def draw_seeds(self):
        for row in range(len(self.seeds)):
            for col in range(len(self.seeds[row])):
                if self.seeds[row][col]:
                    pg.draw.circle(self.game.screen, (255, 255, 255), (self.x + col * CELL_SIZE + CELL_SIZE/2,
                                                                           self.y + row * CELL_SIZE + CELL_SIZE/2), 1)

    def draw_energizers(self):
        for energizer in self.energizers:
            pg.draw.circle(self.game.screen, (255, 255, 255), (self.x + energizer[0] * CELL_SIZE + CELL_SIZE//2,
                                                                   self.y + energizer[1] * CELL_SIZE + CELL_SIZE//2), 4)

    def process_draw(self):
        self.draw_seeds()
        self.draw_energizers()

    def process_collision(self, object): # for pacman only
        for seed in self.seeds:
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
