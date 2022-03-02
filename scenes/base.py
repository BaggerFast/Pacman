from collections import Generator
import pygame as pg
import scenes
from misc.interfaces.igeneric_object import IGenericObject, IEventful, ILogical, IDrawable
from objects.buttons import ButtonController


class BaseScene(IGenericObject):
    # todo сделать регионы во всех сценах на англ

    def __init__(self, game):
        self.game = game
        self.screen: pg.Surface = self.game.screen
        self.objects: list = []
        self._scene_manager = scenes.SceneManager()

    # region публичные методы

    # region реализация интерфейса
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

    def additional_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self._scene_manager.pop()

    # endregion

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    # endregion

    # region приватные методы
    def _create_title(self) -> None:
        pass

    def _button_init(self) -> Generator:
        yield []

    def _create_objects(self) -> None:
        buttons = list(self._button_init())
        if buttons:
            self.objects.append(ButtonController(self.game, buttons))

    def _configurate(self):
        self._create_objects()
        self._create_title()
    # endregion
