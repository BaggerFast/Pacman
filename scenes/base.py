import pygame as pg
from collections import Generator
from misc.base_pattern import BasePattern
from objects.button import ButtonController


class BaseScene(BasePattern):

    def __init__(self, game):
        self.game = game
        self.screen: pg.Surface = self.game.screen
        self.scene_manager = self.game.scene_manager
        self.scenes = self.game.Scenes
        self.objects: list = []
        self.start_logic()
        self.recreate()

    def start_logic(self):
        pass

    def recreate(self):
        self.objects = []
        self.create_objects()
        self.create_title()

    def process_event(self, event: pg.event.Event) -> None:
        for obj in self.objects:
            obj.process_event(event)
        self.additional_event_check(event)

    def process_logic(self) -> None:
        for obj in self.objects:
            obj.process_logic()
        self.additional_logic()

    def process_draw(self) -> None:
        for obj in self.objects:
            obj.process_draw()
        self.additional_draw()

    def create_objects(self) -> None:
        buttons = list(self.button_init())
        if buttons:
            self.objects.append(ButtonController(self.game, buttons))

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.scene_manager.pop()

    def create_title(self) -> None:
        pass

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    def button_init(self) -> Generator:
        yield []
