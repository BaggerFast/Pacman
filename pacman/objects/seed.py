from pygame import Rect, Surface, draw, time

from pacman.data_core import Colors, IDrawable
from pacman.data_core.data_classes import Cell
from pacman.misc import ImgObj
from pacman.skin import SkinEnum
from pacman.storage import SkinStorage


class SeedContainer(IDrawable):
    def __init__(self, seed_data, energizer_data, anim_step: int) -> None:
        super().__init__()
        self.__timer = time.get_ticks()
        self.__anim_step = anim_step
        self.__seeds = self.prepare_seeds(seed_data)
        self.__energizers = self.prepare_energizers(energizer_data)

        self.__ram_img = ImgObj("other/ram")
        self.__yandex_img = ImgObj("other/yandex")

        self.__show_energizer = True
        self.__max_seeds = len(self.__seeds)

    @staticmethod
    def prepare_seeds(seed_data) -> list[Cell]:
        seed = []
        for i in range(len(seed_data)):
            for j in range(len(seed_data[i])):
                if not seed_data[i][j]:
                    continue
                seed.append(Cell(j, i))
        return seed

    @staticmethod
    def prepare_energizers(energizer_data) -> list[Cell]:
        return [Cell(*cell) for cell in energizer_data]

    def __draw_seeds(self, screen) -> None:
        if SkinStorage().equals(SkinEnum.CHROME):
            for seed in self.__seeds:
                self.__ram_img.move_center(*seed.rect.center).draw(screen)
            return
        for seed in self.__seeds:
            draw.circle(screen, Colors.WHITE, seed.rect.center, 1)

    def __draw_energizers(self, screen) -> None:
        if time.get_ticks() - self.__timer > self.__anim_step:
            self.__timer = time.get_ticks()
            self.__show_energizer = not self.__show_energizer
        if not self.__show_energizer:
            return
        if SkinStorage().equals(SkinEnum.CHROME):
            for energizer in self.__energizers:
                self.__yandex_img.move_center(*energizer.rect.center).draw(screen)
            return
        for energizer in self.__energizers:
            draw.circle(screen, Colors.WHITE, energizer.rect.center, 4)

    def draw(self, screen: Surface) -> None:
        self.__draw_seeds(screen)
        self.__draw_energizers(screen)

    def seed_collision(self, rect: Rect) -> bool:
        if not len(self.__seeds):
            return False
        for i, cell in enumerate(self.__seeds):
            if cell.rect.center == rect.center:
                del self.__seeds[i]
                return True
        return False

    def energizer_collision(self, rect: Rect) -> bool:
        for i, energizer in enumerate(self.__energizers):
            if energizer.rect.center == rect.center:
                del self.__energizers[i]
                return True
        return False

    def is_field_empty(self) -> bool:
        return len(self.__seeds) == 0

    def __len__(self):
        return len(self.__seeds)
