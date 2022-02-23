from collections import Generator

import pygame as pg

from misc.interfaces.object_interfaces import IGenericObject, IEventful, ILogical, IDrawable
from objects.buttons import ButtonController


class BaseScene(IGenericObject):

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
            if isinstance(obj, IEventful):
                obj.process_event(event)
        self.additional_event(event)

    def process_logic(self) -> None:
        for obj in self.objects:
            if isinstance(obj, ILogical):
                print(obj)
                obj.process_logic()
        self.additional_logic()

    def process_draw(self) -> None:
        for obj in self.objects:
            if isinstance(obj, IDrawable):
                print(obj)
                obj.process_draw()
        self.additional_draw()

    def create_objects(self) -> None:
        buttons = list(self.button_init())
        if buttons:
            self.objects.append(ButtonController(self.game, buttons))

    def additional_event(self, event: pg.event.Event) -> None:
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
