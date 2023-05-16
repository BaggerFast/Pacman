import pygame as pg

from pacman.data_core import Colors, PathManager
from pacman.data_core.data_classes import Cell
from pacman.data_core.interfaces import IDrawable
from pacman.misc import HIGH_CALORIE_SEEDS
from pacman.objects import MovementObject


class SeedContainer(MovementObject, IDrawable):
    def __init__(self, game, seed_data, energizer_data) -> None:
        super().__init__()
        self.game = game
        self.__seeds = self.prepare_seeds(seed_data)
        self.__energizers = self.prepare_energizers(energizer_data)
        self.__ram_img = pg.image.load(PathManager.get_image_path("ram"))

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
        for seed in self.__seeds:
            if self.game.skins.current.name == "chrome":
                screen.blit(
                    self.__ram_img,
                    seed.rect.center,
                )
                continue
            pg.draw.circle(
                screen,
                Colors.WHITE,
                seed.rect.center,
                1,
            )

    def __draw_energizers(self, screen) -> None:
        if pg.time.get_ticks() - self.game.animate_timer > self.game.time_out:
            self.game.animate_timer = pg.time.get_ticks()
            self.__show_energizer = not self.__show_energizer
        if not self.__show_energizer:
            return
        for energizer in self.__energizers:
            pg.draw.circle(
                screen,
                Colors.WHITE,
                energizer.rect.center,
                4,
            )

    def draw(self, screen: pg.Surface) -> None:
        self.__draw_seeds(screen)
        self.__draw_energizers(screen)

    def seed_collision(self, rect: pg.Rect) -> bool:
        if not len(self.__seeds):
            return False
        for i, cell in enumerate(self.__seeds):
            if cell.rect.center == rect.center:
                del self.__seeds[i]
                return True
        return False

    def energizer_collision(self, rect: pg.Rect) -> bool:
        for i, energizer in enumerate(self.__energizers):
            if energizer.rect.center == rect.center:
                del self.__energizers[i]
                return True
        return False

    def is_field_empty(self) -> bool:
        return len(self.__seeds) == (self.__max_seeds - 10 if HIGH_CALORIE_SEEDS else 0)

    def __len__(self):
        return len(self.__seeds)
