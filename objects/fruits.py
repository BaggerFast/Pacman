import pygame as pg

from enum import auto, IntEnum
from typing import Tuple

from objects.base import BaseObject
from misc.path import PathManager
from misc.constants import CELL_SIZE
from misc.interfaces import IDrawable, ILogical
from misc.sprite_sheet import SpriteSheet

from .image import ImageObject
from .text import Text


class FruitState(IntEnum):
    WAIT = auto()
    DRAW = auto()
    EATEN = auto()
    STATIC = auto()


class Fruit(IDrawable):

    def __init__(self, image: pg.Surface, points: int, pos, index):
        self.__image = image
        self.__index = index
        self.__rect = self.__image.get_rect()
        self.move_center(*self.pos_from_cell(pos))
        self.__points = points

        self.__state = FruitState.WAIT
        self.__start_timer = None

        self.__text = Text(text=str(self.__points), size=10, rect=self.__rect)
        self.__hud = ImageObject(self.__image, (130 + self.__index * 12, 270))

    def __set_state(self, states):
        if self.__state != states:
            self.__state = states
            self.__start_timer = pg.time.get_ticks()

    @property
    def score(self):
        return self.__points

    def get_timer(self):
        return pg.time.get_ticks() - self.__start_timer

    def process_draw(self, screen: pg.Surface) -> None:
        data = {
            FruitState.DRAW: lambda src: src.blit(self.__image, self.__rect),
            FruitState.EATEN: lambda src: self.__text.process_draw(src),
            FruitState.STATIC: lambda src: self.__hud.process_draw(src)
        }
        if self.__state in data:
            data[self.__state](screen)

    def process_logic(self) -> None:
        if self.__start_timer is None:
            self.__start_timer = pg.time.get_ticks()
        data = {
            FruitState.WAIT: lambda: FruitState.DRAW if self.get_timer() >= 9000 else FruitState.WAIT,
            FruitState.EATEN: lambda: FruitState.EATEN if self.get_timer() < 300 else FruitState.STATIC
        }
        if self.__state in data:
            self.__set_state(data[self.__state]())

    def collision(self, obj) -> bool:
        if self.__state is FruitState.DRAW and self.__rect.collidepoint(obj.rect.center):
            self.__set_state(FruitState.EATEN)
            return True
        return False

    @staticmethod
    def pos_from_cell(cell: Tuple[int, int]) -> Tuple[int, int]:
        return cell[0] * CELL_SIZE + CELL_SIZE // 2, cell[1] * CELL_SIZE + 20 + CELL_SIZE // 2

    def move_center(self, x: int, y: int) -> None:
        self.__rect.centerx = x
        self.__rect.centery = y


class FruitController(IDrawable, ILogical):

    def __init__(self, game, pos: tuple):
        # todo delete game
        self.game = game
        self.__cur_index: int = 0
        self.images = SpriteSheet(PathManager.get_image_path('fruits.png'), (14, 14))[0]
        self.scores = (100, 300, 500, 700, 1000, 2000, 3000)
        self.fruits = []
        self.pos = pos
        self.new_fruit()

    # region Public

    # region Implementation of IDrawable, ILogical
    def process_logic(self) -> None:
        for fruit in self.fruits:
            fruit.process_logic()

    def process_draw(self, screen: pg.Surface) -> None:
        for fruit in self.fruits:
            fruit.process_draw(screen)

    # endregion

    def new_fruit(self):
        if not len(self.images) == len(self.scores):
            raise IndexError('Длинна очков не совпадает с длинной фруктов')
        if self.__cur_index not in range(0, len(self.scores)):
            raise IndexError('Кол-во фруктов меньше предполагаемого')
        self.fruits.append(Fruit(self.images[self.__cur_index], self.scores[self.__cur_index],
                                 self.pos, self.__cur_index))

    @property
    def current_image(self) -> Fruit:
        return self.fruits[-1]

    def process_collision(self, obj: BaseObject):
        if self.current_image.collision(obj):
            self.game.sounds.fruit.play()
            self.game.store_fruit(self.__cur_index, 1 * self.game.difficulty)
            self.game.current_scene.score.eat_fruit(self.current_image.score)
            self.__change_image()

    # endregion

    # region Private

    def __change_image(self) -> None:
        self.__cur_index += 1
        self.new_fruit()

    # endregion
