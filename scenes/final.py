from datetime import datetime

from constants import Color
from objects.text import Text
from scenes.base import BaseScene


class FinalScene(BaseScene):
    TEXT_FMT = 'Game over ({})'
    seconds_to_end = 1500

    def __init__(self, game):
        self.last_seconds_passed = 0
        super().__init__(game)
        self.update_start_time()

    def on_activate(self):
        self.update_start_time()

    def update_start_time(self):
        self.time_start = datetime.now()

    def get_gameover_text_formatted(self):
        return self.TEXT_FMT.format(self.seconds_to_end - self.last_seconds_passed)

    def create_objects(self):
        self.text = Text(
            self.game,
            text=self.get_gameover_text_formatted(), color=Color.RED,
            x=self.game.WIDTH // 2, y=self.game.HEIGHT // 2
        )
        self.objects.append(self.text)

    def additional_logic(self):
        time_current = datetime.now()
        seconds_passed = (time_current - self.time_start).seconds
        if self.last_seconds_passed != seconds_passed:
            self.last_seconds_passed = seconds_passed
            self.objects[0].update_text(self.get_gameover_text_formatted())
        if seconds_passed >= self.seconds_to_end:
            self.game.set_scene(self.game.MENU_SCENE_INDEX)

    def on_window_resize(self):
        self.text.move_center(x=self.game.WIDTH // 2, y=self.game.HEIGHT // 2)