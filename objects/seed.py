import pygame as pg
from misc import CELL_SIZE, Color, get_path, HIGH_CALORIE_SEEDS, EvenType
from misc.constants.skin_names import SkinsNames
from objects import DrawableObject


class Seed(DrawableObject):
    def __init__(self, game, rect, image):
        super().__init__(game)
        self.rect = rect
        self.image = image

    @property
    def get_rect(self):
        rect = self.image.get_rect()
        rect.x, rect.y = self.rect[0], self.rect[1]
        return rect

    def check_collision(self, obj):
        return self.get_rect.center == obj.rect.center

    def process_draw(self) -> None:
        self.game.screen.blit(self.image, self.rect)


class SeedContainer(DrawableObject):
    def __init__(self, game, seed_data, energizer_data, x=0, y=20) -> None:
        super().__init__(game)
        self.__ram_img = pg.image.load(get_path("images/ram.png"))
        self.__x = x
        self.__y = y
        self.__seeds = seed_data
        self.__energizers = energizer_data
        self.__color_state: bool = False
        self.__color = {
            True: Color.WHITE,
            False: Color.BLACK
        }
        self.seed_bf = list(self.seed_bufer())

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def seed_bufer(self):
        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if self.__seeds[row][col]:
                    # if self.game.skins.current.name == SkinsNames.chrome:
                    yield Seed(self.game, (self.x - 2 + col * CELL_SIZE, self.y - 2 + row * CELL_SIZE), self.__ram_img)

    def __draw_seeds(self) -> None:
        for seed in self.seed_bf:
            seed.process_draw()

    def __draw_energizers(self) -> None:
        if pg.time.get_ticks() - self.game.animate_timer > self.game.time_out:
            self.game.animate_timer = pg.time.get_ticks()
            self.__color_state = not self.__color_state
        for energizer in self.__energizers:
            pg.draw.circle(self.game.screen, self.__color[self.__color_state],
                           (self.x + energizer[0] * CELL_SIZE + 4,
                            self.y + energizer[1] * CELL_SIZE + 4), 4)

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

        for seed in self.seed_bf:
            if seed.check_collision(obj):
                self.seed_bf.remove(seed)
                if not self.game.sounds.seed.get_busy():
                    self.game.sounds.seed.play()
                pg.event.post(pg.event.Event(EvenType.EatSeed))
                return

        for energizer in self.__energizers:
            if energizer[1] * CELL_SIZE + 18 == obj.rect.y:
                if energizer[0] * CELL_SIZE - 2 == obj.rect.x:
                    self.__energizers.remove(energizer)
                    pg.event.post(pg.event.Event(EvenType.EatEnergizer))
                    return

    def is_field_empty(self) -> bool:
        return not (any([self.seed_bf, self.__energizers]))
