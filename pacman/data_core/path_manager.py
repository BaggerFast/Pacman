import os
from abc import ABC
from os.path import dirname, abspath, join
from typing import Final, List


class Dirs(ABC):
    ROOT: Final[str] = dirname(dirname(dirname(abspath(__file__))))
    ASSET: Final[str] = join(ROOT, "assets")
    IMAGE: Final[str] = join(ASSET, "images")
    SOUND: Final[str] = join(ASSET, "sounds")


class PathManager(ABC):
    @staticmethod
    def get_sound_path(path: str, extension="ogg") -> str:
        pth = join(Dirs.SOUND, path)
        if pth.endswith(f".{extension}"):
            return pth
        return f"{pth}.{extension}"

    @staticmethod
    def get_image_path(path: str, extension="png") -> str:
        pth = join(Dirs.IMAGE, path)
        if pth.endswith(f".{extension}"):
            return pth
        return f"{pth}.{extension}"

    @staticmethod
    def get_asset_path(path: str) -> str:
        return join(Dirs.ASSET, f"{path}")

    @staticmethod
    def get_path(path: str) -> str:
        return join(Dirs.ROOT, path)

    @classmethod
    def get_list_path(cls, path: str, ext: str) -> List[str]:
        path = cls.get_path(path)
        pathes = [f for f in os.listdir(path) if f.endswith(f'.{ext.strip(".")}')]
        pathes.sort(key=lambda x: int(x.strip(f'.{ext.strip(".")}')))
        return [join(path, f) for f in pathes]
