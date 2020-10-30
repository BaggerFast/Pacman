import pygame

from constants import Color
from objects.text import Text
from scenes.base import BaseScene


class PauseScene(BaseScene):
    def create_objects(self):
        self.text = Text(
            game=self.game,
            text='Game paused', color=Color.RED,
            x=self.game.WIDTH // 2, y=self.game.HEIGHT // 2
        )
        self.objects.append(self.text)

    def additional_event_check(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.set_scene(self.game.MAIN_SCENE_INDEX, resume=True)

    def on_window_resize(self):
        self.text.move_center(x=self.game.WIDTH // 2, y=self.game.HEIGHT // 2)
