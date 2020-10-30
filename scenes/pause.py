import pygame

from constants import Color
from objects import TextObject
from scenes import BaseScene


class PauseScene(BaseScene):
    def create_objects(self) -> None:
        self.text = TextObject(
            game=self.game,
            text='Game paused', color=Color.RED,
            x=self.game.WIDTH // 2, y=self.game.HEIGHT // 2
        )
        self.objects.append(self.text)

    def additional_event_check(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.set_scene(self.game.MAIN_SCENE_INDEX, resume=True)

    def on_window_resize(self) -> None:
        self.text.move_center(x=self.game.WIDTH // 2, y=self.game.HEIGHT // 2)
