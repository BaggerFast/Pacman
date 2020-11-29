from random import randint
from typing import Tuple

from misc.constants import Points, CELL_SIZE
from misc.path import get_image_path_for_animator
from misc.animator import Animator
from objects.base import DrawableObject
import pygame as pg


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
        self.__start_time = None
        self.__eat_timer = 90
        self.__score_to_eat = randint(100, 500)

    def __draw_fruit(self):
        if self.__drawing:
            self.screen.blit(self.__anim.current_image, self.rect)

    def __check_score(self):
        if self.__check_last_score():
            self.__drawing = True
            self.__start_time = pg.time.get_ticks()

    def __check_last_score(self):
        if int(self.game.score) >= self.__score_to_eat:
            self.__drawing = True
            return True
        return False

    def __check_time(self):
        if pg.time.get_ticks() - self.__start_time >= 9000:  # 9000
            self.__start_time = None
            self.__score_to_eat = self.self.game.score + self.__eat_timer
            self.__drawing = False
            self.__change_image()

    def __change_image(self) -> None:
        self.__anim.change_cur_image(randint(0, self.__anim.get_len_anim() - 1))

    def process_collision(self, object) -> Tuple[bool, str]:
        """
        :param object: any class with pygame.rect
        :return: is objects in collision (bool) and self type (str)
        """
        if self.__drawing:
            if (self.rect.x == min(object.rect.left, object.rect.right))\
                    and (self.rect.y == object.rect.y):
                self.__drawing = False
                self.__score_to_eat = int(self.game.score) + self.__eat_timer + Points.POINT_PER_FRUIT
                self.__change_image()
                return True, "fruit"
        return False, ""

    def process_logic(self):
        self.__check_score() if self.__drawing else self.__check_score()

    def process_draw(self) -> None:
        self.__draw_fruit()
