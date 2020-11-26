import pygame as pg
from objects import ButtonController, Button, Text
from scenes import BaseScene, GameScene
from misc import Color, Font


class PauseScene(BaseScene):

    def create_objects(self) -> None:
        self.__create_title()
        self.__create_buttons()

    def __create_buttons(self) -> None:
        buttons = [
            Button(self.game, pg.Rect(0, 0, 180, 45),
                   self.continue_game, 'CONTINUE',
                   center=(self.game.width // 2, 100),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 45),
                   self.restart_game, 'RESTART',
                   center=(self.game.width // 2, 161),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 45),
                   self.start_menu, 'MENU',
                   center=(self.game.width // 2, 224),
                   text_size=Font.BUTTON_TEXT_SIZE),
        ]
        self.button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.button_controller)

    def __create_title(self) -> None:
        self.__main_text = Text(self.game, 'PAUSE', 40, color=Color.WHITE, font=Font.FILENAME)
        self.__main_text.move_center(self.game.width // 2, 35)
        self.objects.append(self.__main_text)

    def restart_game(self) -> None:
        self.game.set_scene('SCENE_GAME', reset=True)

    def continue_game(self) -> None:
        self.game.set_scene('SCENE_GAME')

    def start_menu(self) -> None:
        self.game.set_scene('SCENE_MENU')

    def process_event(self, event: pg.event.Event) -> None:
        super().process_event(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.continue_game()

    def on_activate(self) -> None:
        self.button_controller.reset_state()

    def on_deactivate(self) -> None:
        pass
        # self.game.scenes["SCENE_GAME"] = GameScene(self.game)
        # self.game.score.score = 0
