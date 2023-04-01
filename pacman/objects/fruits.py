from random import randint
import pygame as pg
from pacman.data_core import PathManager, Dirs
from pacman.misc.animator import Animator
from pacman.misc.cell_util import CellUtil
from pacman.misc.serializers import MainStorage
from pacman.objects.base import DrawableObject
from pacman.objects import Text, ImageObject


class Fruit(DrawableObject):
    def __init__(self, game, pos: tuple) -> None:
        super().__init__()
        self.game = game
        self.__anim = Animator(PathManager.get_list_path(f"{Dirs.IMAGE}/fruit", ext="png"), False, False)
        self.__image = self.__anim.current_image
        self.rect = self.__anim.current_image.get_rect()
        self.move_center(*CellUtil.pos_from_cell(pos))
        self.__scores = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
        self.__creating_scores()
        self.__drawing = False
        self.__eaten = None
        self.__eaten_time = 0
        self.__start_time = pg.time.get_ticks()
        self.__eat_timer = 90
        self.__score_to_eat = 0
        self.__score_tolerance = 150

    def __draw_fruit(self, screen: pg.Surface):
        if self.__eaten:
            Text(
                text=f"{self.__scores[self.__anim.get_cur_index() - 1]}",
                size=10,
                rect=self.rect,
            ).process_draw(screen)

        if self.__drawing:
            screen.blit(self.__anim.current_image, self.rect)

        for i in range(self.__anim.get_cur_index(), 0, -1):
            ImageObject(
                self.game,
                PathManager.get_image_path(f"fruit/{i-1}"),
                (130 + (i - 1) * 12, 270),
            ).process_draw(screen)

    def __creating_scores(self):
        if len(self.__scores) < self.__anim.get_len_anim():
            for i in range(len(self.__scores) - 1, self.__anim.get_len_anim()):
                self.__scores.append(randint(100, 500))

    def __check_time(self):
        if pg.time.get_ticks() - self.__start_time >= 9000:  # 9000
            self.__drawing = True
            self.__score_to_eat = (
                int(self.game.score) + self.__eat_timer + self.__scores[self.__anim.get_cur_index() - 1]
            )
        if pg.time.get_ticks() - self.__start_time >= 300:
            self.__eaten = None

    def __change_image(self) -> None:
        self.__anim.change_cur_image((self.__anim.get_cur_index() + 1) % self.__anim.get_len_anim())

    def process_collision(self, object):
        if self.__drawing:
            if (self.rect.x == min(object.rect.left, object.rect.right)) and (self.rect.y == object.rect.y):
                self.game.sounds.fruit.play()
                self.__drawing = False
                self.__start_time = pg.time.get_ticks()
                self.__eaten = True
                self.__score_to_eat = (
                    int(self.game.score) + self.__eat_timer + self.__scores[self.__anim.get_cur_index()]
                )
                MainStorage().store_fruit(self.__anim.get_cur_index(), 1)
                self.game.score.eat_fruit(self.__scores[self.__anim.get_cur_index()])
                self.__change_image()

    def process_logic(self):
        self.__check_time()

    def process_draw(self, screen: pg.Surface) -> None:
        self.__draw_fruit(screen)
