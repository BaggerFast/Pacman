import pygame as pg
from objects import ButtonController, Button, Text
from scenes import BaseScene
from misc import Color, Font


class GameoverScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)

    def create_objects(self) -> None:
        self.__create_title()
        self.__create_buttons()
        self.__create_score_text()
        self.__create_highscore_text()

    def __create_title(self) -> None:
        title_game = Text(self.game, 'GAME', 40, color=Color.WHITE, font=Font.FILENAME)
        title_over = Text(self.game, 'OVER', 40, color=Color.WHITE, font=Font.FILENAME)
        title_game.move_center(self.game.width // 2, 30)
        title_over.move_center(self.game.width // 2, 60 + 20)
        self.objects.append(title_game)
        self.objects.append(title_over)

    def __create_buttons(self) -> None:
        buttons = [
            Button(self.game, pg.Rect(0, 0, 180, 35),
                   self.__restart_game, 'RESTART',
                   center=(self.game.width // 2, 210),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 35),
                   self.__start_menu, 'MENU',
                   center=(self.game.width // 2, 250),
                   text_size=Font.BUTTON_TEXT_SIZE)
        ]
        self.__button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.__button_controller)

    def __create_score_text(self) -> None:
        self.__text_score = Text(self.game, f'Score: {self.game.score}', 20, color=Color.WHITE)
        self.__text_score.move_center(self.game.width // 2, 135)
        self.objects.append(self.__text_score)

    def __create_highscore_text(self) -> None:
        self.__text_highscore = Text(self.game, f'High score: {self.game.records.data[-1]}', 20, color=Color.WHITE)
        self.__text_highscore.move_center(self.game.width // 2, 165)
        self.objects.append(self.__text_highscore)

    def on_activate(self) -> None:
        self.__save_record()
        self.__text_score.update_text(f'Score: {self.game.score}')
        self.__text_score.move_center(self.game.width // 2, 135)
        self.__text_highscore.update_text(f'High score: {self.game.records.data[-1]}')
        self.__text_highscore.move_center(self.game.width // 2, 165)
        self.__button_controller.reset_state()

    def __start_menu(self) -> None:
        self.game.set_scene('SCENE_MENU')

    def __restart_game(self) -> None:
        self.game.set_scene('SCENE_GAME', reset=True)

    def additional_event_check(self, event: pg.event.Event) -> None:
        if self.game.scenes[self.game.current_scene_name] == self:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.set_scene('SCENE_MENU')

    def __save_record(self) -> None:
        self.game.records.add_new_record(int(self.game.score))
