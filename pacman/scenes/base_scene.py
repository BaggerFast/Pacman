import pygame as pg
from misc.patterns.entities import PoolEntity
from pacman.scenes.manager import SceneManager


class Scene:

    def __init__(self, game) -> None:
        self.game = game
        self.screen: pg.Surface = self.game.screen
        self.objects: list = []
        self.static_objects = []
        self.create_static_objects()

    def process_event(self, event: pg.event.Event) -> None:
        for item in self.objects:
            item.process_event(event)
        self.additional_event_check(event)

    def process_logic(self) -> None:
        for item in self.objects:
            item.process_logic()
        self.additional_logic()

    def process_draw(self) -> None:
        for item in self.objects:
            item.render()
        self.additional_draw()

    def create_static_objects(self) -> None:
        self.create_title()

    def create_objects(self) -> None:
        self.objects = []
        self.create_buttons()

    def on_activate(self) -> None:
        self.create_objects()

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            SceneManager().pop()

    def additional_logic(self) -> None:
        pass

    def additional_draw(self) -> None:
        for item in self.static_objects:
            item.render()

    def on_deactivate(self) -> None:
        pass

    def on_reset(self) -> None:
        pass

    def create_buttons(self) -> None:
        pass

    def create_title(self) -> None:
        pass

    def recreate(self) -> None:
        self.__init__(self.game)


class BaseScene:

    def __init__(self, game):
        self.game = game
        self.objects = PoolEntity()
        self.recreate()

    def update(self):
        self.objects.update()

    def render(self, screen: pg.Surface):
        self.objects.render(screen)

    def event_handler(self, event: pg.event.Event) -> None:
        self.objects.event_handler(event)

    def recreate(self):
        self._setup_logic()
        if obj := self._create_objects():
            self.objects.append(*list(obj))

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    # region Private

    def _setup_logic(self) -> None:
        pass

    def _create_objects(self) -> None:
        pass

    # endregion
