import pygame as pg
from pacman.data_core import PathManager, Dirs
from pacman.data_core.enums import FruitStateEnum
from pacman.data_core.game_objects import GameObjects
from pacman.data_core.interfaces import IDrawable, ILogical
from pacman.misc.animator import Animator
from pacman.misc.cell_util import CellUtil
from pacman.misc.serializers import MainStorage
from pacman.objects import Text, ImageObject
from pacman.objects.base import MovementObject


class Fruit(MovementObject, IDrawable, ILogical):
    def __init__(self, game, pos: tuple) -> None:
        super().__init__()
        self.game = game
        self.__anim = Animator(PathManager.get_list_path(f"{Dirs.IMAGE}/fruit", ext="png"), False, False)
        self.rect = self.__anim.current_image.get_rect()
        self.move_center(*CellUtil.pos_from_cell(pos))

        self.state = FruitStateEnum.DISABLED
        self.timer = pg.time.get_ticks()

        self.__scores = [100, 300, 500, 700, 1000, 2000, 3000, 5000]

        self.eaten_text = Text(text=f"{self.__scores[self.__anim.get_cur_index()]}", size=10, rect=self.rect)
        self.eaten_fruits_hud = GameObjects()

    def change_state(self, state: FruitStateEnum):
        self.timer = pg.time.get_ticks()
        self.state = state

    def __draw_fruit(self, screen: pg.Surface):
        if self.state is FruitStateEnum.ACTIVE:
            screen.blit(self.__anim.current_image, self.rect)
        elif self.state is FruitStateEnum.EATEN:
            self.eaten_text.draw(screen)
        self.eaten_fruits_hud.draw(screen)

    def __check_time(self):
        if self.state is FruitStateEnum.DISABLED and pg.time.get_ticks() - self.timer >= 9000:
            self.change_state(FruitStateEnum.ACTIVE)
        elif self.state is FruitStateEnum.EATEN and pg.time.get_ticks() - self.timer >= 300:
            self.change_state(FruitStateEnum.DISABLED)

    def __change_image(self) -> None:
        self.eaten_text.text = f"{self.__scores[(self.__anim.get_cur_index() + 1) % self.__anim.get_len_anim()]}"
        self.eaten_fruits_hud.append(
            ImageObject(self.__anim.current_image, (130 + (len(self.eaten_fruits_hud) - 1) * 12, 270))
        )
        self.__anim.change_cur_image((self.__anim.get_cur_index() + 1) % self.__anim.get_len_anim())

    def process_collision(self, rect: pg.Rect):
        if self.state is not FruitStateEnum.ACTIVE:
            return False
        if not (self.rect.y == rect.y and rect.left <= self.rect.x <= rect.right):
            return False
        self.change_state(FruitStateEnum.EATEN)
        MainStorage().store_fruit(self.__anim.get_cur_index(), 1)
        self.game.score.eat_fruit(self.__scores[self.__anim.get_cur_index()])
        self.__change_image()
        return True

    def update(self):
        self.__check_time()

    def draw(self, screen: pg.Surface) -> None:
        self.__draw_fruit(screen)
