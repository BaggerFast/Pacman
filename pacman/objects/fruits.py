from pygame import Rect, Surface, time

from pacman.animator import sprite_slice
from pacman.data_core import IDrawable, ILogical
from pacman.data_core.enums import FruitStateEnum
from pacman.misc import CellUtil, GameObjects, ImgObj, RectObj

from .text import Text


class Fruit(RectObj, IDrawable, ILogical):
    def __init__(self, pos: tuple) -> None:
        self.__fruit_sprite = list(sprite_slice("other/fruits", (12, 12)))[::-1]
        super().__init__(self.__fruit_sprite[0].get_rect())
        self.move_center(*CellUtil.get_center_pos(pos))
        self.state = FruitStateEnum.DISABLED

        self.timer = time.get_ticks()
        self.eaten_text = Text(" ", 10, self.rect)
        self.eaten_fruits_hud = GameObjects()

    def change_state(self, state: FruitStateEnum):
        self.state = state
        self.timer = time.get_ticks()

    def toggle_mode_to_eaten(self, score):
        if not self.__fruit_sprite:
            return
        self.eaten_text.text = f"{score}"
        x_offset = len(self.eaten_fruits_hud)
        pos_x_hud = 130 + x_offset + x_offset * self.rect.width
        self.eaten_fruits_hud.append(ImgObj(self.__fruit_sprite.pop(), (pos_x_hud, 270)))
        self.change_state(FruitStateEnum.EATEN)

    def process_collision(self, rect: Rect) -> bool:
        return self.state == FruitStateEnum.ACTIVE and self.rect.center == rect.center and self.__fruit_sprite

    def update(self):
        if self.state is FruitStateEnum.DISABLED and time.get_ticks() - self.timer >= 9000:
            self.change_state(FruitStateEnum.ACTIVE)
        elif self.state is FruitStateEnum.EATEN and time.get_ticks() - self.timer >= 500:
            self.change_state(FruitStateEnum.DISABLED)

    def draw(self, screen: Surface) -> None:
        if self.state is FruitStateEnum.ACTIVE and self.__fruit_sprite:
            sprite = self.__fruit_sprite[len(self.__fruit_sprite) - 1]
            screen.blit(sprite, self.rect)
        elif self.state is FruitStateEnum.EATEN:
            self.eaten_text.draw(screen)
        self.eaten_fruits_hud.draw(screen)
