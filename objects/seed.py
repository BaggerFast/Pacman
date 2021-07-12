import pygame as pg
import pygame.event

from misc import CELL_SIZE, Color, get_path, HIGH_CALORIE_SEEDS, EvenType
from misc.constants.skin_names import SkinsNames
from objects import DrawableObject


class SeedContainer(DrawableObject):
    def __init__(self, game, seed_data, energizer_data, x=0, y=20) -> None:
        super().__init__(game)
        self.__ram_img = pg.image.load(get_path("ram", "png", "images"))
        self.__x = x
        self.__y = y
        self.__seeds = seed_data
        self.__energizers = energizer_data
        self.__color = {
            -1: Color.WHITE,
            1: Color.BLACK
        }
        self.__index_color = 1
        self.__seeds_on_field = 0
        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if self.__seeds[row][col]:
                    self.__seeds_on_field += 1
        self.__max_seeds = self.__seeds_on_field

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __draw_seeds(self) -> None:
        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if self.__seeds[row][col]:
                    if self.game.skins.current.name == SkinsNames.chrome:
                        # todo universal skins of seed
                        self.game.screen.blit(self.__ram_img, (self.x + col * CELL_SIZE + CELL_SIZE // 2 - 6,
                                                               self.y + row * CELL_SIZE + CELL_SIZE // 2 - 6))
                    else:
                        pg.draw.circle(self.game.screen, Color.WHITE, (self.x + col * CELL_SIZE + CELL_SIZE // 2,
                                                                       self.y + row * CELL_SIZE + CELL_SIZE // 2), 1)

    def __draw_energizers(self) -> None:
        if pg.time.get_ticks() - self.game.animate_timer > self.game.time_out:
            self.game.animate_timer = pg.time.get_ticks()
            self.__index_color *= -1
        for energizer in self.__energizers:
            pg.draw.circle(self.game.screen, self.__color[self.__index_color],
                           (self.x + energizer[0] * CELL_SIZE + CELL_SIZE // 2,
                            self.y + energizer[1] * CELL_SIZE + CELL_SIZE // 2), 4)

    def process_draw(self) -> None:
        self.__draw_seeds()
        self.__draw_energizers()

    def process_collision(self, obj: DrawableObject):
        """
        :param obj: any class with pygame.rect
        :return: is objects in collision (bool) and self type (str)
        """
        if self.is_field_empty():
            pg.event.post(pg.event.Event(EvenType.Win))

        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if self.__seeds[row][col] and row * CELL_SIZE + 18 == obj.rect.y:
                    if col * CELL_SIZE - 2 == obj.rect.x:
                        self.__seeds[row][col] = None
                        if not self.game.sounds.seed.get_busy():
                            self.game.sounds.seed.play()
                        self.__seeds_on_field -= 1
                        pg.event.post(pg.event.Event(EvenType.EatSeed))
                        return
        for energizer in self.__energizers:
            if energizer[1] * CELL_SIZE + 18 == obj.rect.y:
                if energizer[0] * CELL_SIZE - 2 == obj.rect.x:
                    self.__energizers.remove(energizer)
                    pg.event.post(pg.event.Event(EvenType.EatEnergizer))

    def is_field_empty(self) -> bool:
        return self.__seeds_on_field == (self.__max_seeds - 10 if HIGH_CALORIE_SEEDS else 0)
