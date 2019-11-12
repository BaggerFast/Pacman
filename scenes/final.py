from constants import Color
from objects.text import Text
from scenes.base import Scene


class FinalScene(Scene):
    MAX_TICKS = 300
    GAMEOVER_FMT = 'Game over ({})'

    def __init__(self, game):
        self.seconds_left = self.MAX_TICKS // 100
        super().__init__(game)

    def get_gameover_str(self):
        return self.GAMEOVER_FMT.format(self.seconds_left)

    def create_objects(self):
        self.text_gameover = Text(self.game, text=self.get_gameover_str(), color=Color.RED, x=310, y=290)
        self.objects = [self.text_gameover]

    def additional_logic(self):
        self.game.ticks += 1
        seconds_left = self.MAX_TICKS // 100 - self.game.ticks // 100
        if seconds_left < self.seconds_left:  # Оптимизация производительности:
            self.seconds_left = seconds_left  # вызываем font.render только тогда,
            self.text_gameover.update_text(self.get_gameover_str())  # когда текст изменился
        if self.seconds_left == 0:
            self.game.game_over = True