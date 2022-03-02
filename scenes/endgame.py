import pygame as pg
import scenes
from misc.constants import Font, BUTTON_DEFAULT_COLORS
from objects import Text
from objects.buttons import Button


class EndScene(scenes.BaseScene):

    # todo Game is used in __init__
    def __init__(self, game, score):
        super().__init__(game)
        self.score = score

    # region Public

    # region Realization of methods
    def _create_objects(self) -> None:
        super()._create_objects()
        self.objects += [self.__get_score_text, self.__get_highscore_text]

    def _create_title(self) -> None:
        text = Text('VICTORY', 40, font=Font.TITLE)
        text.move_center(self.game.width // 2, 30)
        self.objects.append(text)

    def _button_init(self) -> None:
        yield Button(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 35),
            function=self.__next_level,
            text='NEXT LEVEL',
            center=(self.game.width // 2, 210),
            text_size=Font.BUTTON_TEXT_SIZE,
            colors=BUTTON_DEFAULT_COLORS
        )
        if not self.game.maps.is_last_level():
            yield Button(
                game=self.game,
                rect=pg.Rect(0, 0, 180, 35),
                text='EXIT',
                function=lambda: self._scene_manager.reset(scenes.MainScene(self.game)),
                center=(self.game.width // 2, 210),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=BUTTON_DEFAULT_COLORS
            )
        yield Button(
            game=self.game,
            rect=pg.Rect(0, 0, 180, 35),
            text='MENU',
            function=lambda: self._scene_manager.reset(scenes.MenuScene(self.game)),
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE,
            colors=BUTTON_DEFAULT_COLORS
        )
    # endregion

    def configurate(self):
        self.__save_record()
        self.__unlock_level()

    def on_enter(self) -> None:
        self.game.sounds.siren.stop()
        self.game.sounds.gameover.play()

    def on_exit(self) -> None:
        self.game.sounds.gameover.stop()
    # endregion

    # region Private
    @property
    def __get_score_text(self) -> Text:
        text_score = Text(f'Score: {self.score}', 20)
        text_score.move_center(self.game.width // 2, 135)
        return text_score

    @property
    def __get_highscore_text(self) -> Text:
        text_highscore = Text(f'High score: {self.game.records.data[0]}' if int(self.score) <= self.game.records.data[
            0] else f'New record: {self.score}', 20)
        text_highscore.move_center(self.game.width // 2, 165)
        return text_highscore

    def __save_record(self) -> None:
        self.game.records.add_new_record(int(self.score))
        self.game.records.update_records()

    def __unlock_level(self) -> None:
        if not self.game.maps.is_last_level():
            next_level = self.game.maps.cur_id + 1
            self.game.unlock_level(next_level)

    def __next_level(self) -> None:
        next_level = self.game.maps.cur_id + 1
        self.game.maps.cur_id = next_level
        self.game.records.update_records()
        self._scene_manager.reset(scenes.MainScene(self.game))
    # endregion
