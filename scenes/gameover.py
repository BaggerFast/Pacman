import pygame as pg
from objects import ButtonController, Button, Text
from objects.button.button import SceneButton
from scenes import base
from misc import Color, Font


class Scene(base.Scene):
    def create_static_objects(self):
        self.__create_title()

    def create_objects(self) -> None:
        super().create_objects()
        self.__save_record()
        self.__create_score_text()
        self.__create_highscore_text()

    def __create_title(self) -> None:
        text = ['GAME', 'OVER']
        for i in range(2):
            text[i] = Text(self.game, text[i], 40, font=Font.TITLE)
            text[i].move_center(self.game.width // 2, 30 + i * 40)
            self.static_object.append(text[i])

    def create_buttons(self) -> None:
        names = {
            0: ("RESTART", self.game.scenes.MAIN, True),
            1: ("MENU", self.game.scenes.MENU, False),
        }
        buttons = []
        for i in range(len(names)):
            buttons.append(SceneButton(self.game, pg.Rect(0, 0, 180, 35),
                text=names[i][0],
                scene=(names[i][1], names[i][2]),
                center=(self.game.width // 2, 210+40*i),
                text_size=Font.BUTTON_TEXT_SIZE
            ))
        self.objects.append(ButtonController(self.game, buttons))

    def __create_score_text(self) -> None:
        self.__text_score = Text(self.game, f'Score: {self.game.score}', 20)
        self.__text_score.move_center(self.game.width // 2, 135)
        self.objects.append(self.__text_score)

    def __create_highscore_text(self) -> None:
        self.__text_highscore = Text(self.game, f'High score: {self.game.records.data[-1]}', 20)
        self.__text_highscore.move_center(self.game.width // 2, 165)
        self.objects.append(self.__text_highscore)

    def additional_event_check(self, event: pg.event.Event) -> None:
        if self.game.current_scene == self:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.scenes.set(self.game.scenes.MENU)

    def __save_record(self) -> None:
        self.game.records.add_new_record(int(self.game.score))
