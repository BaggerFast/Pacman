from json import JSONDecodeError, dumps, load

from pygame.event import Event

from pacman.data_core import EvenType, IEventful

from . import LevelStorage, SkinStorage
from .main_storage import MainStorage


class StorageLoader(IEventful):
    def __init__(self, path: str):
        self.__path = path
        self.__saves_on = True

    def to_file(self) -> None:
        if not self.__saves_on:
            return
        string = dumps(MainStorage().serialize(), indent=2)
        with open(self.__path, "w") as f:
            f.write(string)

    def from_file(self) -> None:
        try:
            with open(self.__path, "r") as f:
                MainStorage().deserialize(load(f))

        except (FileNotFoundError, JSONDecodeError):
            self.to_file()

    def event_handler(self, event: Event):
        if event.type == EvenType.UNLOCK_SAVES:
            self.to_file()
            self.__handle_unlock_saves_event(event)
        elif event.type == EvenType.SET_SETTINGS:
            self.to_file()
        elif event.type == EvenType.GET_SETTINGS:
            self.from_file()
            self.__handle_get_settings_event(event)

    def __handle_unlock_saves_event(self, event: Event):
        SkinStorage().event_handler(event)
        LevelStorage().event_handler(event)
        self.__saves_on = False

    def __handle_get_settings_event(self, event: Event):
        if not self.__saves_on:
            SkinStorage().event_handler(event)
            LevelStorage().event_handler(event)
