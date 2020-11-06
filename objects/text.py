import pygame

from objects.base import DrawableObject


class TextObject(DrawableObject):
    def __init__(self, game,
                 font_name: str = 'Comic Sans',
                 font_size: int = 35, is_bold: bool = True, is_italic: bool = False, text: str = 'Define me!',
                 color: pygame.color.Color = (255, 255, 255), x: int = 100, y: int = 100) -> None:
        super().__init__(game)
        self.font_name = font_name
        self.font_size = font_size
        self.is_bold = is_bold
        self.is_italic = is_italic
        self.color = color
        self.font = pygame.font.SysFont(self.font_name, self.font_size, self.is_bold, self.is_italic)
        self.rect = pygame.rect.Rect(x, y, 10, 10)
        self.update_text(text)

    def update_text(self, text: str) -> None:
        self.text = text
        self.surface = self.font.render(self.text, True, self.color)
        x = self.rect.centerx
        y = self.rect.centery
        self.rect = self.surface.get_rect()
        self.move_center(x, y)

    def process_draw(self) -> None:
        self.game.screen.blit(self.surface, self.rect)
