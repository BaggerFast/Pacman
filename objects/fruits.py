from misc.path import get_image_path_for_animator
from misc.animator import Animator
from objects.base import DrawableObject

class Fruit(DrawableObject):
    def __init__(self, game, screen, x, y):
        super().__init__(game)
        self.screen = screen
        self.anim = Animator(get_image_path_for_animator('fruit'), 70, False, False)
        self.image = self.anim.current_image
        self.current_image = self.anim.current_image_index
        self.rect = self.anim.current_image.get_rect()

        self.rect.x = x - self.rect.width / 2
        self.rect.y = y - self.rect.height / 2
        self.image_name = 0

    def draw_fruit(self):
        self.screen.blit(self.image, self.rect)

    def process_collision(self, object):
        if self.rect.x == object.rect.x and self.rect.y == object.rect.y:
            self.image = None
            return True, "energizer"

    def process_logic(self):
        self.draw_fruit()
