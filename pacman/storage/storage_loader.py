from json import JSONDecodeError, dumps, load

from pygame.event import Event

from pacman.data_core import EvenType, IEventful, event_append

from . import LevelStorage, SkinStorage
from .main_storage import MainStorage


class StorageLoader(IEventful):
    def __init__(self, path: str):
        self.__path = path
        self.__cheat_on = False

    def to_file(self) -> None:
        if self.__cheat_on:
            return
        string = dumps(MainStorage().serialize(), indent=2)
        with open(self.__path, "w") as f:
            f.write(string)

    def from_file(self) -> None:
        if self.__cheat_on:
            return
        try:
            with open(self.__path, "r") as f:
                MainStorage().deserialize(load(f))

        except (FileNotFoundError, JSONDecodeError):
            self.to_file()

    def event_handler(self, event: Event):
        if self.__cheat_on:
            return
        if event.type == EvenType.UNLOCK_SAVES:
            self.__handle_unlock_saves_event(event)
        elif event.type == EvenType.SET_SETTINGS:
            self.to_file()
        elif event.type == EvenType.GET_SETTINGS:
            self.from_file()

    def __handle_unlock_saves_event(self, event: Event):
        self.to_file()
        SkinStorage().event_handler(event)
        LevelStorage().event_handler(event)
        self.__cheat_on = True
