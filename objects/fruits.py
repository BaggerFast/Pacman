from misc.constants import Points
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
        self.eat_timer = 90
        self.score_to_eat = self.eat_timer

    def draw_fruit(self):
        if self.drawing:
            self.screen.blit(self.image, self.rect)

    def check_score(self):
        if self.check_last_score():
            self.drawing = True

    def check_last_score(self):
        if self.game.score.score >= self.score_to_eat:
            self.drawing = True
            return 1
        return 0

    def check_time(self):
        pass

    def change_image(self):
        if self.anim.current_image_index + 1 < len(self.anim.images):
            self.anim.change_cur_image(self.anim.current_image_index + 1)
        else:
            self.anim.current_image_index = 0
        self.image = self.anim.current_image

    def process_collision(self, object):
        if self.drawing:
            if ((self.rect.x == object.rect.x + object.rect.width - 3)\
                    or (self.rect.x == object.rect.x - object.rect.width + 3)) \
                    and (self.rect.y == object.rect.y):
                self.drawing = False
                self.score_to_eat = self.game.score.score + self.eat_timer + Points.POINT_PER_FRUIT
                self.change_image()
                return True, "fruit"
        return False, ""

    def process_logic(self):
        self.check_score()

    def process_draw(self):
        self.draw_fruit()
