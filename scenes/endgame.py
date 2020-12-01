import pygame as pg
from objects import ButtonController, Button, Text
from scenes import base, levels
from misc import Color, Font, Maps


class Scene(base.Scene):
    def __init__(self, game):
        super().__init__(game)

    def create_objects(self) -> None:
        self.__create_title()
        self.__create_buttons()
        self.__create_score_text()
        self.__create_highscore_text()

    def __create_title(self) -> None:
        title_game = Text(self.game, 'YOU', 40, font=Font.TITLE)
        title_over = Text(self.game, 'WON', 40, font=Font.TITLE)
        title_game.move_center(self.game.width // 2, 30)
        title_over.move_center(self.game.width // 2, 60 + 20)
        self.objects.append(title_game)
        self.objects.append(title_over)

    def __create_buttons(self) -> None:
        buttons = [
            Button(
                self.game, pg.Rect(0, 0, 180, 35),
                self.__next_level, 'NEXT LEVEL',
                center=(self.game.width // 2, 210),
                text_size=Font.BUTTON_TEXT_SIZE
            )if int(self.game.level_name[-1:]) != Maps.count else Button(
                self.game, pg.Rect(0, 0, 180, 35),
                self.__start_menu, 'EXIT',
                center=(self.game.width // 2, 210),
                text_size=Font.BUTTON_TEXT_SIZE
            ),
            Button(
                self.game, pg.Rect(0, 0, 180, 35),
                self.__start_menu, 'MENU',
                center=(self.game.width // 2, 250),
                text_size=Font.BUTTON_TEXT_SIZE
            )
        ]
        self.__button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.__button_controller)

    def __create_score_text(self) -> None:
        self.__text_score = Text(self.game, f'Score: {self.game.score}', 20)
        self.__text_score.move_center(self.game.width // 2, 135)
        self.objects.append(self.__text_score)

    def __create_highscore_text(self) -> None:
        self.__text_highscore = Text(self.game, f'High score: {self.game.records.data[-1]}', 20)
        self.__text_highscore.move_center(self.game.width // 2, 165)
        self.objects.append(self.__text_highscore)

    def on_activate(self) -> None:
        self.__save_record()
        self.__text_score.text = f'Score: {self.game.score}'
        self.__text_score.move_center(self.game.width // 2, 135)
        self.__text_highscore.text = f'High score: {self.game.records.data[-1]}'
        self.__text_highscore.move_center(self.game.width // 2, 165)
        self.__button_controller.reset_state()

    def __start_menu(self) -> None:
        self.game.set_scene(self.game.scenes.MENU)


    def additional_event_check(self, event: pg.event.Event) -> None:
        if self.game.current_scene == self:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.set_scene(self.game.scenes.MENU)

    def __save_record(self) -> None:
        self.game.records.add_new_record(int(self.game.score))

    def __next_level(self):
        level_number = int(self.game.level_name[-1:])

        next_level = 'level_' + str(level_number+1)
        print(next_level)
        self.game.unlock_level(next_level)
        self.game.level_name = next_level
        self.game.set_scene(self.game.scenes.MAIN,reset=True)

