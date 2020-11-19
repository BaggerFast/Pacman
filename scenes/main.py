import pygame

from misc.constants import Color
from objects.text import Text
from scenes.base import BaseScene


class GameScene(BaseScene):
    def create_objects(self) -> None:
        self.text = Text(self.game, "GAME IS HERE", 30, color=Color.WHITE)
        self.text.move_center(self.game.width // 2, self.game.height // 2)
        self.objects.append(self.text)

    def additional_event_check(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.start_pause()

    def start_pause(self):
        self.game.set_scene(self.game.SCENE_PAUSE)
