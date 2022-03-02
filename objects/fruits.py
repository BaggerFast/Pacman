from typing import List, Tuple
import pygame as pg
from misc.constants import CELL_SIZE
from misc.interfaces import IDrawable, ILogical
from misc.path import get_image_path
from misc.sprite_sheet import SpriteSheet
from objects.base import BaseObject
from .text import Text
from .image import ImageObject


class Fruit(BaseObject, IDrawable, ILogical):

    def __init__(self, game, pos: tuple):
        BaseObject.__init__(self)
        # todo delete game
        self.game = game
        self.images = SpriteSheet(get_image_path('fruits.png'), (14, 14))[0]
        self.__cur_index: int = 0
        self.rect = self.current_image.get_rect()
        self.move_center(*self.pos_from_cell(pos))
        self.is_hidden = False
        self.__scores: List[int] = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
        self.__eaten: bool = False
        self.__start_time = pg.time.get_ticks()
        self.__fruit_hud: List[ImageObject] = []

    # region Public

    # region Implementation of IDrawable, ILogical

    def process_logic(self):
        self.is_hidden = pg.time.get_ticks() - self.__start_time >= 9000
        self.__eaten = not pg.time.get_ticks() - self.__start_time >= 300

    def process_draw(self, screen: pg.Surface) -> None:
        self.__draw_fruit(screen)
        for fruit in self.__fruit_hud:
            fruit.process_draw(screen)

    # endregion

    @property
    def current_image(self) -> pg.Surface:
        return self.images[self.__cur_index]

    def process_collision(self, obj: BaseObject):
        """
        :param obj: any class with pygame.rect
        :return: is objects in collision (bool) and self type (str)
        """
        if not (self.is_hidden and self.rect.collidepoint(obj.rect.center)):
            return
        self.game.sounds.fruit.play()
        self.is_hidden = False
        self.__eaten = True
        self.__start_time = pg.time.get_ticks()
        self.game.store_fruit(self.__cur_index, 1 * self.game.difficulty)

        self.game.current_scene.score.eat_fruit(self.__scores[self.__cur_index])
        self.__change_image()

    @staticmethod
    def pos_from_cell(cell: Tuple[int, int]) -> Tuple[int, int]:
        return cell[0] * CELL_SIZE + CELL_SIZE // 2, cell[1] * CELL_SIZE + 20 + CELL_SIZE // 2

    # endregion

    # region Private

    def __draw_fruit(self, screen: pg.Surface) -> None:
        if self.__eaten:
            Text(text=str(self.__scores[self.__cur_index - 1] * self.game.difficulty),
                 size=10, rect=self.rect).process_draw(screen)
        if self.is_hidden:
            screen.blit(self.current_image, self.rect)

    def __change_image(self) -> None:
        self.__cur_index = (self.__cur_index + 1) % len(self.images)
        self.rect = self.current_image.get_rect(center=self.rect.center)
        self.__fruit_hud.append(ImageObject(self.images[self.__cur_index - 1], (130 + self.__cur_index * 12, 270)))

    # endregion
