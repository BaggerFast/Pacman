from pygame import KEYDOWN
from pygame.event import Event

from pacman.data_core import EvenType, IEventful, KbKeys, event_append


class KbEvent(IEventful):
    def __init__(self):
        self.__kb_down_actions = {
            KbKeys.DOWN: EvenType.DONW_BTN,
            KbKeys.UP: EvenType.UP_BTN,
            KbKeys.ENTER: EvenType.ENTER_BTN,
            KbKeys.LEFT: EvenType.LEFT_BTN,
            KbKeys.RIGHT: EvenType.RIGHT_BTN,
        }

    def event_handler(self, event: Event) -> None:
        if event.type != KEYDOWN:
            return
        for key in self.__kb_down_actions:
            if event.key in key:
                event_append(self.__kb_down_actions[key])
