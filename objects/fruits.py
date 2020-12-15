import pygame as pg
from random import randint
from typing import Tuple

from misc.constants import CELL_SIZE
from misc.path import get_list_path, get_path
from misc.animator import Animator
from objects.base import DrawableObject
from objects import Text, ImageObject


class Fruit(DrawableObject):
    def __init__(self, game, pos: tuple) -> None:
        self.game = game
        super().__init__(game)
        self.screen = game.screen
        self.__anim = Animator(get_list_path('png', 'images', 'fruit'), False, False)
        self.__image = self.__anim.current_image
        self.rect = self.__anim.current_image.get_rect()
        self.move_center(*self.pos_from_cell(pos))
        self.__scores = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
        self.__creating_scores()
        self.__drawing = False
        self.__eaten = None
        self.__eaten_time = 0
        self.__start_time = pg.time.get_ticks()
        self.__eat_timer = 90
        self.__score_to_eat = 0
        self.__score_tolerance = 150

    def __draw_fruit(self):
        if self.__eaten:
            Text(game=self.game, text=str(self.__scores[self.__anim.get_cur_index()-1] * self.game.difficulty), size=10, rect=self.rect).process_draw()

        if self.__drawing:
            self.screen.blit(self.__anim.current_image, self.rect)

        for i in range(self.__anim.get_cur_index(), 0, -1):
            ImageObject(self.game, get_path(str(i-1), 'png', 'images', 'fruit'),
                        (130 + (i-1) * 12, 270)).process_draw()

    def __creating_scores(self):
        if len(self.__scores) < self.__anim.get_len_anim():
            for i in range(len(self.__scores) - 1, self.__anim.get_len_anim()):
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
        if pg.time.get_ticks() - self.__start_time >= 9000:  # 9000
            self.__drawing = True
            self.__score_to_eat = int(self.game.score) + self.__eat_timer + self.__scores[self.__anim.get_cur_index()-1]
        if pg.time.get_ticks() - self.__start_time >= 300:
            self.__eaten = None

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
                self.game.sounds.fruit.play()
                self.__drawing = False
                self.__start_time = pg.time.get_ticks()
                self.__eaten = True
                self.__score_to_eat = int(self.game.score) + self.__eat_timer + self.__scores[
                    self.__anim.get_cur_index()]
                self.game.store_fruit(self.__anim.get_cur_index(), 1 * self.game.difficulty)
                self.game.score.eat_fruit(self.__scores[self.__anim.get_cur_index()])
                self.__change_image()

    def process_logic(self):
        temp = True
        if temp:
            self.__check_time()

    def process_draw(self) -> None:
        self.__draw_fruit()

    @staticmethod
    def pos_from_cell(cell: Tuple[int, int]) -> Tuple[int, int]:
        return cell[0] * CELL_SIZE + CELL_SIZE // 2, cell[1] * CELL_SIZE + 20 + CELL_SIZE // 2
