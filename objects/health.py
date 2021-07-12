from .image import ImageObject
from misc import get_path, EvenType
import pygame


class Health(ImageObject):
    base_pos = (5, 270)
    shift = 20

    def __init__(self, game, lives: int = 3, max_lives: int = 5):
        super().__init__(
            game,
            image=get_path('1', 'png', 'images', 'pacman', game.skins.current.name, 'walk'),
            pos=self.base_pos)
        self.max_lives: int = max_lives
        self.__lives: int = self.__check_limits(lives)
        self.image = pygame.transform.flip(self.image, True, False)

    def __add__(self, value: int) -> "Health":
        self.__lives = self.__check_limits(self.__lives + value)
        return self

    def __sub__(self, value: int) -> "Health":
        self.__lives = self.__check_limits(self.__lives - value)
        return self

    def __iadd__(self, value: int) -> "Health": return self + value
    def __isub__(self, value: int) -> "Health": return self - value
    def __index__(self) -> int: return int(self)
    def __int__(self) -> int: return self.__lives
    def __check_limits(self, value) -> int: return max(-1, min(self.max_lives, int(value)))
    def add(self, value: int) -> None:  self.__lives = self.__check_limits(self.__lives + value)

    def process_draw(self):
        self.game.screen.blits((self.image, (self.rect.x + i * self.shift, self.rect.y)) for i in range(self))

    def process_event(self, event: pygame.event.Event):
        if event.type == EvenType.HealthInc:
            self + 1
        elif event.type == EvenType.HealthDec:
            self - 1

    def process_logic(self):
        if not self.game.cheats_var.INFINITY_LIVES and int(self) < 0:
            if(not self.game.sounds.pacman.get_busy()) and (not self.game.sounds.intro.get_busy()):
                pygame.event.post(pygame.event.Event(EvenType.GameOver))

