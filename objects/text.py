import pygame

from objects.base import DrawableObject


class Text(DrawableObject):
    def __init__(self, game, font_name='Comic Sans', font_size=35, is_bold=True, is_italic=False, text='Define me!',
                 color=(255, 255, 255), x=100, y=100):
        super().__init__(game)
        self.font_name = font_name
        self.font_size = font_size
        self.is_bold = is_bold
        self.is_italic = is_italic
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(self.font_name, self.font_size, self.is_bold, self.is_italic)
        self.update_text(text)

    def update_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
        self.move_center(self.x, self.y)

    def process_draw(self):
        self.game.screen.blit(self.surface, self.rect)
