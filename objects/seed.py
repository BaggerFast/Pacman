import pygame

from objects.base import DrawableObject


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
        self.energizer_data = energizer_data

    def draw_seeds(self):
        for row in range(len(self.seeds)):
            for col in range(len(self.seeds[row])):
                if self.seeds[row][col]:
                    pygame.draw.circle(self.game.screen, (255, 255, 255), (self.x + col * 8 + 4, self.y + row * 8 + 4), 1)

    def draw_energizers(self):
        for energizer in self.energizer_data:
            pygame.draw.circle(self.game.screen, (255, 255, 255), (self.x + energizer[0] * 8 + 4, self.y + energizer[1] * 8 + 4), 4)

    def process_draw(self):
        self.draw_seeds()
        self.draw_energizers()