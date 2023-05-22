from pacman.data_core import Dirs, PathUtl
from pacman.misc import LevelLoader

from .map import Map


class MapViewLoader:
    def __init__(self):
        self.__images = {}
        self.__levels_pathes = sorted(PathUtl.get_list(f"{Dirs.ASSET}/maps"))
        self.__count = len(self.__levels_pathes)

    def get_view(self, level_id: int) -> Map:
        level_id = abs(level_id)
        if abs(level_id) > self.__count - 1:
            raise ValueError("Map level id not valid")
        if level_id not in self.__images:
            loader = LevelLoader(self.__levels_pathes[level_id]).map
            self.__images[level_id] = Map(loader)
        return self.__images[level_id]
