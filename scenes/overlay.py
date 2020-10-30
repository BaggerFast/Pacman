from datetime import datetime

from constants import Color
from objects import TextObject
from scenes import BaseScene


class OverlayScene(BaseScene):
    last_datetime = datetime.now()
    current_datetime = datetime.now()

    def create_objects(self) -> None:
        self.text = TextObject(
            game=self.game,
            text='FPS', color=Color.YELLOW,
            x=self.game.WIDTH-50, y=15
        )
        self.objects.append(self.text)

    def additional_logic(self) -> None:
        self.last_datetime = self.current_datetime
        self.current_datetime = datetime.now()
        delta = self.current_datetime - self.last_datetime
        milliseconds = int(delta.total_seconds() * 1000)
        if milliseconds != 0:
            fps = 1000 / milliseconds
            self.text.update_text(str(int(fps)))
        else:
            self.text.update_text('inf')

    def on_window_resize(self) -> None:
        self.text.move_center(x=self.game.WIDTH-50, y=15)
