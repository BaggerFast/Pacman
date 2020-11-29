from random import randint
from typing import Tuple

from misc import Points, CELL_SIZE
from misc.path import get_list_path
from misc.animator import Animator
from objects.base import DrawableObject


class Fruit(DrawableObject):
    def __init__(self, game, screen, x, y) -> None:
        super().__init__(game)
        self.screen = screen
        self.__anim = Animator(get_list_path('images/fruit', 'png'), False, False)
        self.__image = self.__anim.current_image
        self.rect = self.__anim.current_image.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y - self.rect.height // 2
        self.__drawing = False
        self.__eat_timer = 90
        self.__score_to_eat = 0

    def __draw_fruit(self) -> None:
        if self.__drawing:
            self.screen.blit(self.__anim.current_image, self.rect)

    def __check_score(self) -> None:
        if self.__check_last_score():
            self.__drawing = True

    def __check_last_score(self) -> bool:
        if self.game.score.score >= self.__score_to_eat:
            self.__drawing = True
            return True
        return False

    def __change_image(self) -> None:
        self.__anim.change_cur_image(randint(0, self.__anim.get_len_anim() - 1))

    def process_collision(self, object) -> Tuple[bool, str]:
        """
        :param object: any class with pygame.rect
        :return: is objects in collision (bool) and self type (str)
        """
        if self.__drawing:
            if ((self.rect.x == object.rect.x + object.rect.width - CELL_SIZE//2)\
                    or (self.rect.x == object.rect.x - object.rect.width + CELL_SIZE//2)) \
                    and (self.rect.y == object.rect.y):
                self.__drawing = False
                self.__score_to_eat = self.game.score.score + self.__eat_timer + Points.POINT_PER_FRUIT
                self.__change_image()
                return True, "fruit"
        return False, ""

    def process_logic(self) -> None:
        self.__check_score()

    def process_draw(self) -> None:
        self.__draw_fruit()
