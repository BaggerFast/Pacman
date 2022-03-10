import pygame as pg

from misc import Animator, PathManager
from misc.constants import EvenType, event_append, CELL_SIZE, SkinsNames
from misc.interfaces import IDrawable
from misc.sprite_sheet import SpriteSheet


class SeedAnimator(Animator):
    def __init__(self, images: list[pg.Surface], time_out: int = 50,
                 repeat: bool = False, aura: str = None):
        super().__init__(images, time_out, repeat, aura)

    def timer_check(self) -> None:
        self.current_index += 1
        self.image_swap()


class Seed(IDrawable):

    def __init__(self, game, rect, image):
        # todo delete game
        self.game = game
        self.rect = rect
        self.image = image

    @property
    def get_rect(self):
        rect = self.image.get_rect()
        rect.x, rect.y = self.rect[0], self.rect[1]
        return rect

    def check_collision(self, obj):
        return self.get_rect.center == obj.rect.center

    def process_draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)

    def remove(self):
        event_append(EvenType.EAT_SEED)
        if not self.game.sounds.seed.is_busy():
            self.game.sounds.seed.play()


class BigSeed(Seed):
    def __init__(self, game, rect):
        # todo delete game
        path = 'big_seed.png' if game.skins.current.name != SkinsNames.chrome else "big_seed_google.png"
        self.animator = SeedAnimator(SpriteSheet(PathManager.get_image_path(path), (9, 9))[0])
        super().__init__(game, rect, self.animator.current_image)

    def remove(self):
        event_append(EvenType.EAT_ENERGIZER)
        if not self.game.sounds.seed.is_busy():
            self.game.sounds.seed.play()

    def process_draw(self, screen: pg.Surface) -> None:
        screen.blit(self.animator.current_image, self.rect)


class SeedContainer(IDrawable):

    def __init__(self, game, seed_data, energizer_data, x=0, y=20) -> None:
        self.game = game
        self.__ram_img = pg.image.load(PathManager.get_image_path("ram.png"))
        self.__x = x
        self.__y = y
        self.seed_bf = list(self.seed_buffer(seed_data))
        self.big_seed_bf = list(self.big_seed_buffer(energizer_data))

    def seed_buffer(self, data):
        for row in range(len(data)):
            for col in range(len(data[row])):
                if data[row][col]:
                    yield Seed(self.game, (self.__x - 2 + col * CELL_SIZE, self.__y - 2 + row * CELL_SIZE),
                               self.__ram_img)

    def big_seed_buffer(self, data):
        for energizer in data:
            yield BigSeed(self.game, (self.__x + energizer[0] * CELL_SIZE, self.__y + energizer[1] * CELL_SIZE))

    def __draw_seeds(self, screen: pg.Surface) -> None:
        for seed in self.seed_bf:
            seed.process_draw(screen)

    def __draw_energizers(self, screen: pg.Surface) -> None:
        flag = pg.time.get_ticks() - self.game.animate_timer > self.game.time_out
        if flag:
            self.game.animate_timer = pg.time.get_ticks()
        for seed in self.big_seed_bf:
            if flag:
                seed.animator.timer_check()
            seed.process_draw(screen)

    def process_draw(self, screen: pg.Surface) -> None:
        self.__draw_seeds(screen)
        self.__draw_energizers(screen)

    def process_collision(self, obj):
        if self.is_field_empty():
            event_append(EvenType.WIN)
            return

        self.__seed_remover(self.seed_bf, obj)
        self.__seed_remover(self.big_seed_bf, obj)

    def __seed_remover(self, seeds: list[Seed], obj) -> None:
        for seed in seeds:
            if seed.check_collision(obj):
                seed.remove()
                seeds.remove(seed)
                return

    def is_field_empty(self) -> bool:
        return not (any([self.seed_bf, self.big_seed_bf]))
