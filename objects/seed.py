import pygame as pg
from misc import Animator, get_path, SkinsNames, CELL_SIZE, EvenType, event_append
from misc.sprite_sheet import SpriteSheet
from objects.base import DrawableObject


class SeedAnimator(Animator):
    def __init__(self, images: list[pg.Surface], game, time_out: int = 50,
                 repeat: bool = False, aura: str = None):
        self.game = game
        super().__init__(images, time_out, repeat, aura)

    def timer_check(self) -> None:
        self.current_index += 1
        self.image_swap()


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


class BigSeed(Seed):
    def __init__(self, game, rect):
        path = 'images/big_seed.png' if game.skins.current.name != SkinsNames.chrome else "images/big_seed_google.png"
        self.animator = SeedAnimator(SpriteSheet(get_path(path), (9, 9))[0], game)
        super().__init__(game, rect, self.animator.current_image)

    def process_draw(self) -> None:
        self.game.screen.blit(self.animator.current_image, self.rect)


class SeedContainer(DrawableObject):
    def __init__(self, game, seed_data, energizer_data, x=0, y=20) -> None:
        super().__init__(game)
        self.__ram_img = pg.image.load(get_path("images/ram.png"))
        self.__x = x
        self.__y = y
        self.seed_bf = list(self.seed_bufer(seed_data))
        self.big_seed_bf = list(self.big_seed_buffer(energizer_data))

    def seed_bufer(self, data):
        for row in range(len(data)):
            for col in range(len(data[row])):
                if data[row][col]:
                    yield Seed(self.game, (self.__x - 2 + col * CELL_SIZE, self.__y - 2 + row * CELL_SIZE), self.__ram_img)

    def big_seed_buffer(self, data):
        for energizer in data:
            yield BigSeed(self.game,  (self.__x + energizer[0] * CELL_SIZE, self.__y + energizer[1] * CELL_SIZE))

    def __draw_seeds(self) -> None:
        for seed in self.seed_bf:
            seed.process_draw()

    def __draw_energizers(self) -> None:
        flag = pg.time.get_ticks() - self.game.animate_timer > self.game.time_out
        if flag:
            self.game.animate_timer = pg.time.get_ticks()
        for seed in self.big_seed_bf:
            if flag:
                seed.animator.timer_check()
            seed.process_draw()

    def process_draw(self) -> None:
        self.__draw_seeds()
        self.__draw_energizers()

    def process_collision(self, obj: DrawableObject):
        """
        :param obj: any class with pygame.rect
        :return: is objects in collision (bool) and self type (str)
        """
        if self.is_field_empty():
            event_append(EvenType.Win)

        for seed in self.seed_bf:
            if seed.check_collision(obj):
                self.seed_bf.remove(seed)
                event_append(EvenType.EatSeed)
                if not self.game.sounds.seed.get_busy():
                    self.game.sounds.seed.play()
                return

        for seed in self.big_seed_bf:
            if seed.check_collision(obj):
                self.big_seed_bf.remove(seed)
                event_append(EvenType.EatEnergizer)

    def is_field_empty(self) -> bool:
        return not (any([self.seed_bf, self.big_seed_bf]))
