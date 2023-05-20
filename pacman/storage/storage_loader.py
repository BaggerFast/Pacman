from json import JSONDecodeError, dumps, load

from pygame.event import Event

from pacman.data_core import EvenType, IEventful

from .main_storage import MainStorage


class StorageLoader(IEventful):
    def __init__(self, path: str):
        self.__path = path

    def to_file(self) -> None:
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
        if event.type == EvenType.SET_SETTINGS:
            self.to_file()
        elif event.type == EvenType.GET_SETTINGS:
            self.from_file()
