from misc.path import get_image_path_for_animator
from misc.animator import Animator
from objects.base import DrawableObject


class Fruit(DrawableObject):
    def __init__(self, game, screen, x, y):
        super().__init__(game)
        self.screen = screen
        self.anim = Animator(get_image_path_for_animator('fruit'), 70, False, False)
        self.image = self.anim.current_image
        self.image_name = 0
        self.rect = self.anim.current_image.get_rect()
        self.rect.x = x - self.rect.width / 2
        self.rect.y = y - self.rect.height / 2
        self.drawing = False

    def draw_fruit(self):
        if self.drawing:
            self.screen.blit(self.image, self.rect)

    # Фрукт появляется каждые 90 очков (в оригинале 70)
    def check_score(self, score):
        if (score > 0) and (score % 90 == 0):
            self.drawing = True

    def check_time(self):
        pass
    # Тут будет таймер, пока время не вышло
    # - фрукт рисуется и пакман может его съесть

    def change_image(self):
        if self.anim.current_image_index + 1 < len(self.anim.images):
            self.anim.change_cur_image(self.anim.current_image_index + 1)
        else:
            self.anim.current_image_index = 0
        self.image = self.anim.current_image

    def process_collision(self, object):
        if ((self.rect.x == object.rect.x + object.rect.width - 3) \
                or (self.rect.x == object.rect.x - object.rect.width + 3)) \
                and (self.rect.y == object.rect.y):
            self.drawing = False
            self.change_image()
            return True, "energizer"

    def process_logic(self):
        self.draw_fruit()
