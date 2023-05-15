from copy import copy

from pygame import Surface, time

from pacman.objects import ImageObject
from pacman.scenes.base_scene import BaseScene


class BlurScene(BaseScene):

    def __init__(self, game, blur_surface: Surface):
        super().__init__(game)
        self.blur_time = self._start_time
        self._blur_surface = ImageObject(copy(blur_surface), (0, 0))
        self._blur_count = 1
        self._blur_finished = False

    def process_logic(self) -> None:
        if not self._blur_finished:
            blur_time = time.get_ticks() / 1000
            min_blur = min((blur_time - self._start_time) * self._blur_count * 4, self._blur_count)
            self._blur_surface.blur(min_blur)
            self._blur_finished = min_blur == self._blur_count
        super().process_logic()

    def draw(self) -> Surface:
        self._blur_surface.draw(self._screen)
        self.objects.draw(self._screen)
        return self._screen
