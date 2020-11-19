import sys

import pygame
from objects.button import Button
from objects.text import Text
from scenes.base import BaseScene
from misc.constants import Color, BUTTON_DEFAULT_COLORS


class MenuScene(BaseScene):
    def create_objects(self) -> None:

        # Создание и обработка текста
        self.main_text = Text(self.game, 'Pacman', 40, color=Color.WHITE)
        self.main_text.move_center(self.game.width // 2, 30)
        self.objects.append(self.main_text)

        # Создание и обработка кнопок

        # self.continue_button = Button(self.game, pygame.Rect(0, 0, 180, 60),
        #     self.start_game, 'CONTINUE', **BUTTON_COLORS)
        # self.continue_button.move_center(self.game.width // 2, 226)
        # self.objects.append(self.continue_button)

        self.play_button = Button(
            self.game, pygame.Rect(0, 0, 180, 45),
            self.start_game, 'PLAY', **BUTTON_DEFAULT_COLORS
        )
        self.play_button.move_center(self.game.width // 2, 100)
        self.objects.append(self.play_button)

        self.records_button = Button(
            self.game, pygame.Rect(0, 0, 180, 45),
            self.start_records, 'RECORDS', **BUTTON_DEFAULT_COLORS
        )
        self.records_button.move_center(self.game.width // 2, 163)
        self.objects.append(self.records_button)

        self.exit_button = Button(
            self.game, pygame.Rect(0, 0, 180, 45),
            sys.exit, 'EXIT', **BUTTON_DEFAULT_COLORS
        )
        self.exit_button.move_center(self.game.width // 2, 226)
        self.objects.append(self.exit_button)

    def start_game(self):
        self.game.set_scene(self.game.SCENE_GAME)

    def start_records(self):
        self.game.set_scene(self.game.SCENE_RECORDS)