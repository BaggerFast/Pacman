from pygame import Surface
from pygame.event import Event
from pygame import time

from pacman.data_core import Config, Colors
from pacman.data_core.game_objects import GameObjects


class BaseScene:
    def __init__(self, game):
        self.game = game
        self._start_time = time.get_ticks() / 1000
        self.pre_init()
        self._screen = Surface(tuple(Config.RESOLUTION))
        self.objects = GameObjects()

    def pre_init(self):
        pass

    # region Public

    # region Implementation of IGenericObject

    def process_event(self, event: Event) -> None:
        self.objects.event_handler(event)

    def process_logic(self) -> None:
        self.objects.update()

    def draw(self) -> Surface:
        self._screen.fill(Colors.BLACK)
        self.objects.draw(self._screen)
        return self._screen

    # endregion

    def _create_objects(self):
        self.objects.clear()

    def configure(self) -> None:
        self._create_objects()

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    # endregion

    # region Private

    def _create_title(self) -> None:
        pass

    # def _button_init(self):
    #     yield None
    #

    # endregion
