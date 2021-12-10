import pygame as pg
from objects import Text
from objects.button import Button
from misc import BUTTON_DEFAULT_COLORS, Font
from scenes.base import BaseScene


class EndScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.score = 0

    def create_objects(self) -> None:
        super().create_objects()
        self.__save_record()
        self.__create_score_text()
        self.__create_highscore_text()
        self.__unlock_level()

    def create_title(self) -> None:
        text = Text(self.game, 'VICTORY', 40, font=Font.TITLE)
        text.move_center(self.game.width // 2, 30)
        self.static_objects.append(text)

    def button_init(self) -> None:
        yield Button(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 35),
            function=self.__next_level,
            text='NEXT LEVEL',
            center=(self.game.width // 2, 210),
            text_size=Font.BUTTON_TEXT_SIZE,
            colors=BUTTON_DEFAULT_COLORS
        )
        if not self.__is_last_level():
            yield Button(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 35),
                text='EXIT',
                function=self.game.scenes.MENU,
                center=(self.game.width // 2, 210),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=BUTTON_DEFAULT_COLORS
            )
        yield Button(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 35),
            text='MENU',
            function=self.game.scenes.MENU,
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE,
            colors=BUTTON_DEFAULT_COLORS
        )

    def __create_score_text(self) -> None:
        text_score = Text(self.game, f'Score: {self.score}', 20)
        text_score.move_center(self.game.width // 2, 135)
        self.objects.append(text_score)

    def __create_highscore_text(self) -> None:
        text_highscore = Text(self.game, f'High score: {self.game.records.data[0]}'if int(self.score) <= self.game.records.data[0] else f'New record: {self.score}', 20)
        text_highscore.move_center(self.game.width // 2, 165)
        self.objects.append(text_highscore)

    def __save_record(self) -> None:
        self.game.records.add_new_record(int(self.score))
        self.game.records.update_records()

    def __unlock_level(self) -> None:
        if self.__is_last_level():
            next_level = self.game.maps.cur_id + 1
            self.game.unlock_level(next_level)

    def __next_level(self) -> None:
        next_level = self.game.maps.cur_id + 1
        self.game.maps.cur_id = next_level
        self.game.records.update_records()
        self.game.scenes.MAIN(reset=True)

    def __is_last_level(self) -> bool:
        return (self.game.maps.cur_id + 1) < self.game.maps.count

    def on_activate(self) -> None:
        super().on_activate()
        self.game.sounds.siren.stop()
        self.game.sounds.gameover.play()

    def on_deactivate(self) -> None:
        self.game.sounds.gameover.stop()

    def __call__(self, *args, **kwargs):
        self.game.scenes.set(self, reset=True)
