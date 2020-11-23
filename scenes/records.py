import pygame as pg

from misc.constants import Color, Font
from misc.path import get_image_path
from objects.button import Button
from objects.button import ButtonController
from objects.image import ImageObject
from objects.text import Text
from scenes.base import BaseScene


class RecordsScene(BaseScene):
    def create_objects(self) -> None:
        self.create_title()
        self.create_error_label()
        self.create_text_labels()
        self.create_medals()
        self.create_buttons()

    def create_text_labels(self) -> None:
        self.game.records.update_records()
        self.one_text = Text(self.game, str(self.game.records.data[4]), 30, (60, 55), Color.GOLD)
        self.two_text = Text(self.game, str(self.game.records.data[3]), 30, (60, 85), Color.SILVER)
        self.three_text = Text(self.game, str(self.game.records.data[2]), 30, (60, 120), Color.BRONZE)
        self.four_text = Text(self.game, str(self.game.records.data[1]), 30, (60, 155), Color.WHITE)
        self.five_text = Text(self.game, str(self.game.records.data[0]), 30, (60, 190), Color.WHITE)

    def create_medals(self) -> None:
        self.gold_medal = ImageObject(self.game, get_image_path('1_golden', 'medal'), 16, 55)
        self.gold_medal.scale(35, 35)
        self.silver_medal = ImageObject(self.game, get_image_path('2_silver', 'medal'), 16, 85)
        self.silver_medal.scale(35, 35)
        self.bronze_medal = ImageObject(self.game, get_image_path('3_bronze', 'medal'), 16, 120)
        self.bronze_medal.scale(35, 35)
        self.stone_medal = ImageObject(self.game, get_image_path('4_stone', 'medal'), 16, 155)
        self.stone_medal.scale(35, 35)
        self.wooden_medal = ImageObject(self.game, get_image_path('5_wooden', 'medal'), 16, 190)
        self.wooden_medal.scale(35, 35)

    def create_buttons(self) -> None:
        self.back_button = Button(self.game, pg.Rect(0, 0, 180, 40),
                                  self.start_menu, 'MENU', center=(self.game.width // 2, 250),
                                  text_size=Font.BUTTON_TEXT_SIZE)
        self.button_controller = ButtonController(self.game, [self.back_button])
        self.objects.append(self.button_controller)

    def create_title(self) -> None:
        title = Text(self.game, 'RECORDS', 32, color=Color.WHITE, font=Font.FILENAME)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def create_error_label(self) -> None:
        self.error_text = Text(self.game, 'NO RECORDS', 24, color=Color.RED)
        self.error_text.move_center(self.game.width // 2, 100)

    def start_menu(self) -> None:
        self.game.set_scene("SCENE_MENU")

    def on_activate(self) -> None:
        self.button_controller.reset_state()

    def process_draw(self) -> None:
        super().process_draw()

        if self.game.records.data[4] == 0:
            self.error_text.process_draw()

        if self.game.records.data[4] != 0:
            self.one_text.process_draw()
            self.gold_medal.process_draw()

        if self.game.records.data[3] != 0:
            self.two_text.process_draw()
            self.silver_medal.process_draw()

        if self.game.records.data[2] != 0:
            self.three_text.process_draw()
            self.bronze_medal.process_draw()

        if self.game.records.data[1] != 0:
            self.four_text.process_draw()
            self.stone_medal.process_draw()

        if self.game.records.data[0] != 0:
            self.five_text.process_draw()
            self.wooden_medal.process_draw()

    def additional_event_check(self, event: pg.event.Event) -> None:
        if self.game.scenes[self.game.current_scene_name] == self:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.set_scene('SCENE_MENU')
