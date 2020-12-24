import pygame as pg
from objects import ButtonController, Text
from scenes import base
from misc import Font, BUTTON_DEFAULT_COLORS


class Scene(base.Scene):
    def create_objects(self) -> None:
        super().create_objects()
        self.__save_record()
        self.__create_score_text()
        self.__create_highscore_text()

    def create_title(self) -> None:
        text = ['GAME', 'OVER']
        for i in range(2):
            text[i] = Text(self.game, text[i], 40, font=Font.TITLE)
            text[i].move_center(self.game.width // 2, 30 + i * 40)
            self.static_objects.append(text[i])

    def create_buttons(self) -> None:
        names = [
            ("RESTART", self.game.scenes.MAIN),
            ("MENU", self.game.scenes.MENU),
        ]
        buttons = []
        for i, f in enumerate(names):
            buttons.append(self.SceneButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 180, 35),
                text=f[0],
                scene=f[1],
                center=(self.game.width // 2, 210+40*i),
                text_size=Font.BUTTON_TEXT_SIZE,
                colors=BUTTON_DEFAULT_COLORS
            ))
        self.objects.append(ButtonController(self.game, buttons))

    def __create_score_text(self) -> None:
        self.__text_score = Text(self.game, f'Score: {self.game.score}', 20)
        self.__text_score.move_center(self.game.width // 2, 135)
        self.objects.append(self.__text_score)

    def __create_highscore_text(self) -> None:
        self.__text_highscore = Text(self.game, f'High score: {self.game.records.data[-1]}'
                                     if int(self.game.score) <= self.game.records.data[-1] else f'New record: {self.game.score}', 20)
        self.__text_highscore.move_center(self.game.width // 2, 165)
        self.objects.append(self.__text_highscore)

    def __save_record(self) -> None:
        self.game.records.add_new_record(int(self.game.score))

    def on_deactivate(self) -> None:
        self.game.sounds.gameover.stop()

    def on_activate(self) -> None:
        super().on_activate()
        self.game.sounds.pacman.stop()
        self.game.sounds.gameover.play()
