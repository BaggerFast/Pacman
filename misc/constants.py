import pygame

# https://www.pygame.org/docs/ref/color.html
# https://github.com/pygame/pygame/blob/master/src_py/colordict.py

class Color:
    RED = pygame.color.Color('red')
    BLUE = pygame.color.Color('blue')
    GREEN = pygame.color.Color('green')
    BLACK = pygame.color.Color('black')
    WHITE = pygame.color.Color('white')
    ORANGE = pygame.color.Color('orange')
    YELLOW = pygame.color.Color('yellow')
    GOLD = (255, 215, 0)
    SILVER = (192, 192, 192)
    BRONZE = (205, 127, 50)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)


BUTTON_DEFAULT_COLORS = {
    'static_text_color': Color.GRAY,
    'static_button_color': Color.DARK_GRAY,
    'hover_text_color': Color.WHITE,
    'hover_button_color': Color.DARK_GRAY,
    'clicked_text_color': Color.BLACK,
    'clicked_button_color': Color.DARK_GRAY
}