import pygame as pg
from typing import Tuple
from misc import CELL_SIZE
from misc.sprite_sheet import SpriteSheet
from objects.base import BaseObject
from objects import Text, ImageObject
from typing import List


class Fruit(BaseObject):
    def __init__(self, game, pos: tuple) -> None:
        super().__init__(game)
        self.images = SpriteSheet('images/fruits.png', (14, 14))[0]
        self.cur_index: int = 0
        self.rect = self.current_image.get_rect()
        self.move_center(*self.pos_from_cell(pos))
        self.__scores: List[int] = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
        self.__eaten: bool = False
        self.__start_time = pg.time.get_ticks()
        self.fruit_hud: List[ImageObject] = []

    @property
    def current_image(self):
        return self.images[self.cur_index]

    def __draw_fruit(self):
        if self.__eaten:
            Text(game=self.game, text=str(self.__scores[self.cur_index - 1] * self.game.difficulty),
                 size=10, rect=self.rect).process_draw()
        if self.is_hidden:
            self.game.screen.blit(self.current_image, self.rect)

    def __change_image(self):
        self.cur_index = (self.cur_index + 1) % len(self.images)
        self.rect = self.current_image.get_rect(center=self.rect.center)
        self.fruit_hud.append(ImageObject(self.game, self.images[self.cur_index-1], (130 + self.cur_index * 12, 270)))

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
        self.game.store_fruit(self.cur_index, 1 * self.game.difficulty)
        self.game.current_scene.score.eat_fruit(self.__scores[self.cur_index])
        self.__change_image()

    def process_logic(self):
        self.is_hidden = pg.time.get_ticks() - self.__start_time >= 9000
        self.__eaten = not (pg.time.get_ticks() - self.__start_time >= 300)

    def process_draw(self) -> None:
        self.__draw_fruit()
        for fruit in self.fruit_hud:
            fruit.process_draw()

    @staticmethod
    def pos_from_cell(cell: Tuple[int, int]) -> Tuple[int, int]:
        return cell[0] * CELL_SIZE + CELL_SIZE // 2, cell[1] * CELL_SIZE + 20 + CELL_SIZE // 2
