import os
import pygame

from misc.path import get_image_path
from objects.button import Button
from objects.image import ImageObject
from objects.text import Text
from scenes.base import BaseScene
from misc.constants import Color


class RecordsScene(BaseScene):
    def create_objects(self) -> None:
        self.records = self.game.records.data
        self.screen_width = self.screen.get_width()

        # Создание и обработка текста
        self.main_text = Text(self.game, 'RECORDS', 30, color=Color.WHITE)
        self.main_text.move_center(self.screen_width // 2, 25)
        self.objects.append(self.main_text)

        # Создание и обработка рекордов
        self.one_text = Text(self.game, str(self.records[4]), 30, (60, 45), Color.GOLD)
        self.objects.append(self.one_text)

        self.two_text = Text(self.game, str(self.records[3]), 30, (60, 80), Color.SILVER)
        self.objects.append(self.two_text)

        self.three_text = Text(self.game, str(self.records[2]), 30, (60, 115), Color.BRONZE)
        self.objects.append(self.three_text)

        self.four_text = Text(self.game, '4: ' + str(self.records[1]), 30,(25, 150), Color.WHITE)
        self.objects.append(self.four_text)

        self.five_text = Text(self.game, '5: ' + str(self.records[0]), 30,(25, 185), Color.WHITE)
        self.objects.append(self.five_text)

        # Создание и обработка кнопок
        self.back_button = Button(
            self.game, pygame.Rect(self.screen_width // 2, 200, 120, 60),
            self.start_menu, 'BACK', Color.GRAY,
            Color.DARK_GRAY, Color.WHITE, Color.DARK_GRAY,
            Color.BLACK, Color.DARK_GRAY
        )
        self.back_button.move_center(self.screen_width // 2, 250)
        self.objects.append(self.back_button)

        # Создание и обработка изображений
        self.gold_medal = ImageObject(self.game, get_image_path('golden_medal.png'), 16, 45)
        self.gold_medal.scale(35, 35)
        self.objects.append(self.gold_medal)

        self.silver_medal = ImageObject(self.game, get_image_path('silver_medal.png'), 16, 80)
        self.silver_medal.scale(35, 35)
        self.objects.append(self.silver_medal)

        self.bronze_medal = ImageObject(self.game, get_image_path('bronze_medal.png'), 16, 115)
        self.bronze_medal.scale(35, 35)
        self.objects.append(self.bronze_medal)

    def additional_event_check(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.start_menu()

    def start_menu(self):
        self.game.set_scene(self.game.SCENE_MENU)