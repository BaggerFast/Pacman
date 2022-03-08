import pygame as pg
import scenes
from misc.interfaces.igeneric_object import IGenericObject
from objects.buttons import ButtonController
from objects.objects import Objects


class BaseScene(IGenericObject):

    # todo Game is used in __init__
    def __init__(self, game):
        self.game = game
        self.screen: pg.Surface = self.game.screen
        self._scene_manager = scenes.SceneManager()
        self.objects = Objects()

    # region Public

    # region Implementation of IGenericObject

    def process_event(self, event: pg.event.Event) -> None:
        self.objects.process_event(event)

    def process_logic(self) -> None:
        self.objects.process_logic()

    def process_draw(self, screen: pg.Surface) -> None:
        self.objects.process_draw(screen)

    def additional_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self._scene_manager.pop()

    # endregion

    def configurate(self) -> None:
        self._create_objects()
        self._create_title()

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    # endregion

    # region Private

    def _create_title(self) -> None:
        pass

    def _button_init(self):
        yield None

    def _create_objects(self) -> None:
        buttons = list(self._button_init())
        if buttons:
            self.objects.append(ButtonController(self.game, buttons))

    # endregion
