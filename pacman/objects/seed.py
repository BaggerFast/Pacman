from math import floor

from pygame import SRCALPHA, Rect, Surface, draw, time

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
        self.__seeds: list[list[bool]] = self.prepare_seeds(seed_data)
        self.__energizers = self.prepare_energizers(energizer_data)

        self.__buffer = Surface((len(self.__seeds[0]) * 8, len(self.__seeds) * 8 + 20), SRCALPHA)

        self.__ram_img = ImgObj("other/ram")
        self.__yandex_img = ImgObj("other/yandex")

        self.__show_energizer = True
        self.__seeds_counts = sum(sum(i) for i in self.__seeds)
        self.__max_seeds = len(self.__seeds)

    @staticmethod
    def prepare_seeds(seed_data) -> list[list[bool]]:
        seed: list[list[bool]] = [[False] * len(seed_data[0]) for _ in range(len(seed_data))]
        for y in range(len(seed_data)):
            for x in range(len(seed_data[y])):
                seed[y][x] = seed_data[y][x]
        return seed

    @staticmethod
    def prepare_energizers(energizer_data) -> list[Cell]:
        return [Cell(*cell) for cell in energizer_data]

    def __draw_seeds(self, screen) -> None:
        if SkinStorage().equals(SkinEnum.CHROME):
            for y in range(len(self.__seeds)):
                for x in range(len(self.__seeds[y])):
                    if self.__seeds[y][x]:
                        cell = Cell(x, y)
                        self.__ram_img.move_center(*cell.rect.center).draw(screen)
            return
        for y in range(len(self.__seeds)):
            for x in range(len(self.__seeds[y])):
                if self.__seeds[y][x]:
                    cell = Cell(x, y)
                    draw.circle(screen, Colors.WHITE, cell.rect.center, 1)

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

    def create_buffer(self):
        self.__draw_seeds(self.__buffer)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.__buffer, (0, 0))
        self.__draw_energizers(screen)

    def seed_collision(self, rect: Rect) -> bool:
        if not len(self.__seeds):
            return False
        cell = Cell(floor(rect.centerx / 8), floor((rect.centery - 20) / 8))
        if self.__seeds[cell.y][cell.x] and cell.rect.center == rect.center:
            self.__seeds[cell.y][cell.x] = False
            draw.rect(self.__buffer, (0, 0, 0, 0), cell)
            self.__seeds_counts -= 1
            return True
        return False

    def energizer_collision(self, rect: Rect) -> bool:
        for i, energizer in enumerate(self.__energizers):
            if energizer.rect.center == rect.center:
                del self.__energizers[i]
                return True
        return False

    def is_field_empty(self) -> bool:
        return self.__seeds_counts == 0

    def __len__(self):
        return len(self.__seeds)
