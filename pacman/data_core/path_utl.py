from abc import ABC
from os import listdir
from os.path import abspath, dirname, join
from typing import Final, List


class Dirs(ABC):
    ROOT: Final[str] = dirname(dirname(dirname(abspath(__file__))))
    ASSET: Final[str] = join(ROOT, "assets")
    IMAGE: Final[str] = join(ASSET, "images")
    SOUND: Final[str] = join(ASSET, "sounds")


class PathUtl(ABC):
    @staticmethod
    def get_asset(path: str) -> str:
        return join(Dirs.ASSET, f"{path}")

    @staticmethod
    def get_sound(path: str, extension="ogg") -> str:
        pth = join(Dirs.SOUND, path)
        if pth.endswith(f".{extension}"):
            return pth
        return f"{pth}.{extension}"

    @staticmethod
    def get_img(path: str, extension="png") -> str:
        pth = join(Dirs.IMAGE, path)
        if pth.endswith(f".{extension}"):
            return pth
        return f"{pth}.{extension}"

    @staticmethod
    def get(path: str) -> str:
        return join(Dirs.ROOT, path)

    @classmethod
    def get_list(cls, path: str) -> List[str]:
        path = cls.get(path)
        return [join(path, file) for file in listdir(path)]
