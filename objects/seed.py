import pygame as pg

from misc.constants import CELL_SIZE, Color, SOUNDS
from objects.base import DrawableObject
from misc.path import get_sound_path


class SeedContainer(DrawableObject):
    eaten_sound = pg.mixer.Sound(get_sound_path(SOUNDS["Seed"]))
    eaten_sound.set_volume(0.5)
    def __init__(self, game, seed_data, energizer_data, x=0, y=20):
        super().__init__(game)
        self.x = x
        self.y = y
        self.seeds = seed_data
        self.energizers = energizer_data
        self.anim = 0

    def draw_seeds(self):
        for row in range(len(self.seeds)):
            for col in range(len(self.seeds[row])):
                if self.seeds[row][col]:
                    pg.draw.circle(self.game.screen, Color.WHITE, (self.x + col * CELL_SIZE + CELL_SIZE//2,
                                                                           self.y + row * CELL_SIZE + CELL_SIZE//2), 1)

    def draw_energizers(self):
        if self.anim < 8:
            color = Color.WHITE
        else:
            color = Color.BLACK
            if self.anim > 16:
                self.anim = 0
        for energizer in self.energizers:
            pg.draw.circle(self.game.screen, color, (self.x + energizer[0] * CELL_SIZE + CELL_SIZE//2,
                                                                   self.y + energizer[1] * CELL_SIZE + CELL_SIZE//2), 4)
        self.anim += 1

    def process_draw(self):
        self.draw_seeds()
        self.draw_energizers()

    def process_collision(self, object): #for pacman only
        for row in range(len(self.seeds)):
            for col in range(len(self.seeds[row])):
                if self.seeds[row][col] and row * CELL_SIZE + 18 == object.rect.y:
                    if col * CELL_SIZE - 2 == object.rect.x:
                        self.seeds[row][col] = None
                        self.eaten_sound.play()
                        return True, "seed"
        for energizer in self.energizers:
            if energizer[1] * CELL_SIZE + 18 == object.rect.y:
                if energizer[0] * CELL_SIZE - 2 == object.rect.x:
                    self.energizers.remove(energizer)
                    return True, "energizer"
        return False, ""
