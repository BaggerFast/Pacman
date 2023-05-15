from copy import copy

from pygame import Surface, time

from pacman.objects import ImageObject
from pacman.scenes.base_scene import BaseScene


class BlurScene(BaseScene):

    def __init__(self, game, blur_surface):
        super().__init__(game)
        self.blur_time = self._start_time
        self.__blur_surface = ImageObject(copy(blur_surface))
        self.__blur_surface.blur(4)

    def _create_objects(self):
        super()._create_objects()
        self.objects.append(self.__blur_surface)

    def draw(self) -> Surface:
        self.__blur_surface.draw(self._screen)
        return super().draw()
