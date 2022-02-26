from collections import Generator

import pygame as pg

import scenes
from misc.interfaces.igeneric_object import IGenericObject, IEventful, ILogical, IDrawable
from objects.buttons import ButtonController


class BaseScene(IGenericObject):

    def __init__(self, game):
        self.game = game
        self.screen: pg.Surface = self.game.__screen
        self._scene_manager = scenes.SceneManager()
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
                obj.process_logic()
        self.additional_logic()

    def process_draw(self, screen: pg.Surface) -> None:
        for obj in self.objects:
            if isinstance(obj, IDrawable):
                obj.process_draw(screen)
        self.additional_draw(screen)

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
