from abc import ABC
from copy import copy

from pygame import Surface, time

from pacman.misc import ImgObj

from .base_scene import BaseScene


class BlurScene(BaseScene, ABC):
    def __init__(self, blur_surface: Surface):
        super().__init__()
        self._blur_count = 1
        self._blur_finished = False
        self._blur_surface = ImgObj(copy(blur_surface), (0, 0))

    def process_logic(self) -> None:
        if not self._blur_finished:
            blur_time = time.get_ticks() / 1000
            min_blur = min((blur_time - self._start_time) * self._blur_count * 4, self._blur_count)
            self._blur_surface.blur(min_blur)
            self._blur_finished = min_blur == self._blur_count
        super().process_logic()

    def draw(self) -> Surface:
        self._blur_surface.draw(self._screen)
        self._objects.draw(self._screen)
        return self._screen
