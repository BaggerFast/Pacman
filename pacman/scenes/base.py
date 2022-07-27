import pygame as pg
from loguru import logger
from pacman import scenes
from pacman.misc.interfaces import IGenericObject
from pacman.objects.buttons import ButtonController
from pacman.objects.objects import Objects


class BaseScene(IGenericObject):

    # todo Game is used in __init__
    def __init__(self, game):
        self.game = game
        self.screen: pg.Surface = self.game.screen
        self._scene_manager = scenes.SceneManager.instance
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

    def configure(self) -> None:
        self._create_objects()
        self._create_title()

    def on_enter(self) -> None:
        logger.info(f'Set scene: {self.__class__.__name__}')

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
            self.objects.append(ButtonController(buttons))

    # endregion
