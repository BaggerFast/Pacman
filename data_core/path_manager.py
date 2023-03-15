import os
from abc import ABC
from typing import Final, List


class Dirs(ABC):
    ROOT: Final[str] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ASSET: Final[str] = os.path.join(ROOT, "assets")
    IMAGE: Final[str] = os.path.join(ASSET, "images")
    SOUND: Final[str] = os.path.join(ASSET, "sounds")


class PathManager(ABC):
    @staticmethod
    def get_sound_path(path: str, extension="ogg") -> str:
        pth = os.path.join(Dirs.SOUND, path)
        if pth.endswith(f".{extension}"):
            return pth
        return f"{pth}.{extension}"

    @staticmethod
    def get_image_path(path: str, extension="png") -> str:
        pth = os.path.join(Dirs.IMAGE, path)
        if pth.endswith(f".{extension}"):
            return pth
        return f"{pth}.{extension}"

    @staticmethod
    def get_asset_path(path: str) -> str:
        return os.path.join(Dirs.ASSET, f"{path}")

    @staticmethod
    def get_path(path: str) -> str:
        return os.path.join(Dirs.ROOT, path)

    @classmethod
    def get_list_path(cls, path: str, ext: str) -> List[str]:
        path = cls.get_path(path)
        pathes = [f for f in os.listdir(path) if f.endswith(f'.{ext.strip(".")}')]
        pathes.sort(key=lambda x: x.split(f'.{ext.strip(".")}'))
        return [os.path.join(path, f) for f in pathes]
