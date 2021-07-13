import pygame as pg
from typing import Tuple
from misc.constants import CELL_SIZE
from misc.path import get_list_path, get_path
from misc.animator import Animator
from objects.base import DrawableObject
from objects import Text, ImageObject


class Fruit(DrawableObject):
    def __init__(self, game, pos: tuple) -> None:
        super().__init__(game)
        self.__anim = Animator(get_list_path('png', 'images', 'fruit'), False, False)
        self.rect = self.__anim.current_image.get_rect()
        self.move_center(*self.pos_from_cell(pos))
        self.__scores: list[int] = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
        self.__drawing: bool = False
        self.__eaten: bool = False
        self.__start_time = pg.time.get_ticks()
        self.drew_fruits: list[ImageObject] = []

    def __draw_fruit_desk(self):
        if self.__eaten:
            Text(game=self.game, text=str(self.__scores[self.__anim.get_cur_index() - 1] * self.game.difficulty),
                 size=10, rect=self.rect).process_draw()
        if self.__drawing:
            self.game.screen.blit(self.__anim.current_image, self.rect)

    def __check_time(self):
        self.__drawing = pg.time.get_ticks() - self.__start_time >= 9000
        self.__eaten = not (pg.time.get_ticks() - self.__start_time >= 300)

    def __change_image(self) -> None:  # __change_image
        self.__anim.change_cur_image((self.__anim.get_cur_index() + 1) % self.__anim.get_len_anim())

        self.drew_fruits.append(ImageObject(self.game, get_path(str(self.__anim.get_cur_index() - 1), 'png', 'images',
                                                                'fruit'),
                                            (130 + self.__anim.get_cur_index() * 12, 270)))

    def process_collision(self, obj):
        """
        :param obj: any class with pygame.rect
        :return: is objects in collision (bool) and self type (str)
        """
        if not self.__drawing:
            return
        if (self.rect.x == min(obj.rect.left, obj.rect.right)) and (self.rect.y == obj.rect.y):
            self.game.sounds.fruit.play()
            self.__drawing = False
            self.__eaten = True
            self.__start_time = pg.time.get_ticks()
            self.game.store_fruit(self.__anim.get_cur_index(), 1 * self.game.difficulty)
            self.game.current_scene.score.eat_fruit(self.__scores[self.__anim.get_cur_index()])
            self.__change_image()

    def process_logic(self) -> None:
        self.__check_time()

    def process_draw(self) -> None:
        self.__draw_fruit_desk()
        for fruit in self.drew_fruits:
            fruit.process_draw()

    @staticmethod
    def pos_from_cell(cell: Tuple[int, int]) -> Tuple[int, int]:
        return cell[0] * CELL_SIZE + CELL_SIZE // 2, cell[1] * CELL_SIZE + 20 + CELL_SIZE // 2
