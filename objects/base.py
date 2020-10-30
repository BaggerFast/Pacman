import pygame


class DrawableObject:     # TODO: bring here pygame.sprite.Sprite inheritance
    def __init__(self, game):
        self.game = game
        self.rect = pygame.rect.Rect(0, 0, 0, 0)

    def move(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def move_center(self, x, y):
        self.x = x
        self.y = y
        self.rect.centerx = x
        self.rect.centery = y

    def process_event(self, event):
        pass

    def process_logic(self):
        pass

    def process_draw(self):
        pass  # use self.game.screen for drawing, padawan