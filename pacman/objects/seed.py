import pygame as pg
from pacman.data_core import Colors, PathManager
from pacman.data_core.interfaces import IDrawable
from pacman.misc import CELL_SIZE, HIGH_CALORIE_SEEDS
from pacman.objects import MovementObject


class SeedContainer(MovementObject, IDrawable):

    def __init__(self, game, seed_data, energizer_data, x=0, y=20) -> None:
        super().__init__()
        self.game = game
        self.__seeds = seed_data
        self.__energizers = energizer_data
        self.__x, self.__y = x, y

        self.__ram_img = pg.image.load(PathManager.get_image_path("ram"))

        self.__show_energizer = True
        self.__seeds_on_field = sum([1 for seed_row in self.__seeds for seed in seed_row if seed])
        self.__max_seeds = self.__seeds_on_field

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __draw_seeds(self, screen) -> None:
        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if self.__seeds[row][col]:
                    if self.game.skins.current.name == "chrome":
                        screen.blit(
                            self.__ram_img,
                            (
                                self.x + col * CELL_SIZE + CELL_SIZE // 2 - 6,
                                self.y + row * CELL_SIZE + CELL_SIZE // 2 - 6,
                            ),
                        )
                    else:
                        pg.draw.circle(
                            screen,
                            Colors.WHITE,
                            (
                                self.x + col * CELL_SIZE + CELL_SIZE // 2,
                                self.y + row * CELL_SIZE + CELL_SIZE // 2,
                            ),
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
                (
                    self.x + energizer[0] * CELL_SIZE + CELL_SIZE // 2,
                    self.y + energizer[1] * CELL_SIZE + CELL_SIZE // 2,
                ),
                4,
            )

    def draw(self, screen: pg.Surface) -> None:
        self.__draw_seeds(screen)
        self.__draw_energizers(screen)

    def seed_collision(self, rect: pg.Rect) -> bool:
        if not self.__seeds_on_field:
            return False
        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if col * CELL_SIZE - 2 == rect.x and self.__seeds[row][col] and row * CELL_SIZE + 18 == rect.y:
                    self.__seeds[row][col] = False
                    self.__seeds_on_field -= 1
                    return True
        return False

    def energizer_collision(self, rect: pg.Rect) -> bool:
        for energizer in self.__energizers:
            if energizer[1] * CELL_SIZE + 18 == rect.y:
                if energizer[0] * CELL_SIZE - 2 == rect.x:
                    self.__energizers.remove(energizer)
                    return True
        return False

    def is_field_empty(self) -> bool:
        return self.__seeds_on_field == (self.__max_seeds - 10 if HIGH_CALORIE_SEEDS else 0)
