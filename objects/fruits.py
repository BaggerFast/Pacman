from random import randint

from misc.constants import Points, CELL_SIZE
from misc.path import get_image_path_for_animator
from misc.animator import Animator
from objects.base import DrawableObject


class Fruit(DrawableObject):
    def __init__(self, game, screen, x, y):
        super().__init__(game)
        self.screen = screen
        self.__anim = Animator(get_image_path_for_animator('fruit'), False, False)
        self.__image = self.__anim.current_image
        self.rect = self.__anim.current_image.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y - self.rect.height // 2
        self.__drawing = False
        self.__eat_timer = 90
        self.__score_to_eat = 0

    def __draw_fruit(self):
        if self.__drawing:
            self.screen.blit(self.__anim.current_image, self.rect)

    def __check_score(self):
        if self.__check_last_score():
            self.__drawing = True

    def __check_last_score(self):
        if self.game.score.score >= self.__score_to_eat:
            self.__drawing = True
            return 1
        return 0

    def __change_image(self):
        self.__anim.change_cur_image(randint(0, self.__anim.get_len_anim() - 1))

    def process_collision(self, object):
        if self.__drawing:
            if ((self.rect.x == object.rect.x + object.rect.width - CELL_SIZE//2)\
                    or (self.rect.x == object.rect.x - object.rect.width + CELL_SIZE//2)) \
                    and (self.rect.y == object.rect.y):
                self.__drawing = False
                self.__score_to_eat = self.game.score.score + self.__eat_timer + Points.POINT_PER_FRUIT
                self.__change_image()
                return True, "fruit"
        return False, ""

    def process_logic(self):
        self.__check_score()

    def process_draw(self):
        self.__draw_fruit()
