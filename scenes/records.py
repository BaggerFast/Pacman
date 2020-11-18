import pygame

from misc.path import get_image_path
from objects.button import Button, ButtonControl
from objects.image import ImageObject
from objects.text import Text
from scenes.base import BaseScene
from misc.constants import Color, BUTTON_DEFAULT_COLORS


class RecordsScene(BaseScene):
    def create_objects(self) -> None:

        self.current_button = -1

        self.records = self.game.records.data
        self.screen_width = self.screen.get_width()

        # Создание и обработка текста
        self.main_text = Text(self.game, 'RECORDS', 30, color=Color.WHITE)
        self.main_text.move_center(self.screen_width // 2, 25)
        self.objects.append(self.main_text)

        self.error_text = Text(self.game, 'NO RECORDS', 30, color=Color.RED)
        self.error_text.move_center(self.game.width // 2, 100)

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
            self.game, pygame.Rect(self.screen_width // 2, 200, 120, 45),
            self.start_menu, 'BACK', **BUTTON_DEFAULT_COLORS
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

        self.stone_medal = ImageObject(self.game, get_image_path('stone_medal.png'), 16, 150)
        self.stone_medal.scale(35, 35)
        self.objects.append(self.stone_medal)

        self.wooden_medal = ImageObject(self.game, get_image_path('wooden_medal.png'), 16, 185)
        self.wooden_medal.scale(35, 35)
        self.objects.append(self.wooden_medal)

        self.buttons = []
        self.buttons.append(self.back_button)

        self.control = ButtonControl(self.buttons)

    def additional_event_check(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.start_menu()
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.current_button -= 1
                if self.current_button < 0:
                    self.current_button = 0
                self.control.set_current_button(self.current_button)
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.current_button += 1
                if self.current_button > 0:
                    self.current_button = 0
                self.control.set_current_button(self.current_button)
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.buttons[self.current_button].on_click()

    def process_draw(self):
        self.main_text.process_draw()
        if self.records[4] != 0:
            self.one_text.process_draw()
            self.gold_medal.process_draw()
        else:
            self.error_text.process_draw()

        if self.records[3] != 0:
            self.two_text.process_draw()
            self.silver_medal.process_draw()

        if self.records[2] != 0:
            self.three_text.process_draw()
            self.bronze_medal.process_draw()

        if self.records[1] != 0:
            self.four_text.process_draw()
            self.stone_medal.process_draw()

        if self.records[0] != 0:
            self.five_text.process_draw()
            self.wooden_medal.process_draw()

        self.back_button.process_draw()

    def start_menu(self):
        self.game.set_scene(self.game.SCENE_MENU)