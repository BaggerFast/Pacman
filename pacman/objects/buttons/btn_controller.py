from pygame import KEYUP, Surface
from pygame.event import Event

from pacman.data_core import EvenType, IDrawable, IEventful, KbKeys
from pacman.data_core.enums import BtnStateEnum
from pacman.misc import GameObjects

from .btn import Btn


class BtnController(IDrawable, IEventful):
    def __init__(self, buttons: list[Btn], active_index: int = 0):
        self.__buttons = GameObjects()
        self.__buttons.extend(buttons)

        self.__active_button_index = abs(active_index) % len(self.__buttons)
        self.__current.select()

        self.__kb_down_actions = {
            EvenType.DONW_BTN: self.__move_down,
            EvenType.UP_BTN: self.__move_up,
            EvenType.ENTER_BTN: lambda: self.__current.activate(),
        }

    # region Public

    def draw(self, screen: Surface) -> None:
        if self.__current.is_state(BtnStateEnum.INITIAL):
            self.__current.select()
        for button in self.__buttons:
            button.draw(screen)

    def event_handler(self, event: Event) -> None:
        self.__buttons.event_handler(event)
        self.__check_hover_btn()
        self.__parse_keyboard(event)

    # endregion

    # region Private

    @property
    def __current(self) -> Btn:
        return self.__buttons[self.__active_button_index]

    def __move_up(self) -> None:
        self.__current.deselect()
        self.__active_button_index = (self.__active_button_index - 1) % len(self.__buttons)
        self.__current.select()

    def __move_down(self) -> None:
        self.__current.deselect()
        self.__active_button_index = (self.__active_button_index + 1) % len(self.__buttons)
        self.__current.select()

    def __unpress_cur_btn(self) -> None:
        if not self.__current.is_state(BtnStateEnum.CLICK):
            return
        self.__current.select()
        self.__current.click()

    def __parse_keyboard(self, event: Event) -> None:
        if event.type in self.__kb_down_actions:
            self.__kb_down_actions[event.type]()
        elif event.type == KEYUP:
            if event.key in KbKeys.ENTER:
                self.__unpress_cur_btn()

    def __check_hover_btn(self) -> None:
        for index, button in enumerate(self.__buttons):
            if button.is_state(BtnStateEnum.HOVER):
                self.__active_button_index = index
                return

    # endregion
