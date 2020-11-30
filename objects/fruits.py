import pygame as pg
from random import randint
from typing import Tuple

from misc.constants import Points, CELL_SIZE, Sounds
from misc.path import get_list_path
from misc.animator import Animator
from objects.base import DrawableObject


class Fruit(DrawableObject):
    eaten_sound = Sounds.FRUIT

    def __init__(self, game, screen, x, y) -> None:
        super().__init__(game)
        self.screen = screen
        self.__anim = Animator(get_list_path('images/fruit', 'png'), False, False)
        self.__image = self.__anim.current_image
        self.rect = self.__anim.current_image.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y - self.rect.height // 2
        self.__scores = []
        self.__creating_scores()
        self.__drawing = False
        self.__start_time = pg.time.get_ticks()
        self.__eat_timer = 90
        self.__score_to_eat = 0
        self.__score_tolerance = 150
        self.eaten_sound.set_volume(1)

    def __draw_fruit(self):
        if self.__drawing:
            self.screen.blit(self.__anim.current_image, self.rect)

    def __creating_scores(self):
        for i in range(self.__anim.get_len_anim()):
            self.__scores.append(randint(100, 500))

    def __check_score(self):
        if self.__check_last_score():
            return True
        return False

    def __check_last_score(self):
        if int(self.game.score) >= self.__score_to_eat + self.__score_tolerance:
            return True
        return False

    def __check_time(self):
        # print(pg.time.get_ticks(), self.__start_time)
        if pg.time.get_ticks() - self.__start_time >= 9000:  # 9000
            self.__drawing = True
            self.__score_to_eat = int(self.game.score) + self.__eat_timer + self.__scores[self.__anim.get_cur_index()]

    def __change_image(self) -> None:  # __change_image
        self.__anim.change_cur_image((self.__anim.get_cur_index() + 1) % self.__anim.get_len_anim())

    def process_collision(self, object):
        """
        :param object: any class with pygame.rect
        :return: is objects in collision (bool) and self type (str)
        """
        if self.__drawing:
            if (self.rect.x == min(object.rect.left, object.rect.right)) \
                    and (self.rect.y == object.rect.y):
                self.__drawing = False
                self.__start_time = pg.time.get_ticks()
                if not pg.mixer.Channel(0).get_busy():
                    self.eaten_sound.play()
                self.__score_to_eat = int(self.game.score) + self.__eat_timer + self.__scores[
                    self.__anim.get_cur_index()]
                self.__change_image()
                self.game.score.eat_fruit(self.__scores[self.__anim.get_cur_index()])

    def process_logic(self):
        temp = self.__check_score()
        if temp:
            self.__check_time()

    def process_draw(self) -> None:
        self.__draw_fruit()
