import os
from typing import Final


class PathManager:
    ROOT: Final = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ASSET: Final = os.path.join(ROOT, 'assets')
    IMAGE: Final = os.path.join(ASSET, 'images')
    SOUND: Final = os.path.join(ASSET, 'sounds')

    @classmethod
    def get(cls, path: str) -> str:
        return os.path.join(cls.ROOT, path)

    @classmethod
    def get_sound(cls, path: str) -> str:
        return os.path.join(cls.SOUND, path)

    @classmethod
    def get_asset(cls, path) -> str:
        return os.path.join(cls.ASSET, path)

    @classmethod
    def get_image(cls, path) -> str:
        return os.path.join(cls.IMAGE, path)

    @classmethod
    def get_list(cls, path: str, ext: str) -> list[str]:
        path = cls.get(path)
        pathes = [f for f in os.listdir(path) if f.endswith(f'.{ext.strip(".")}')]
        pathes.sort(key=lambda x: x.split(f'.{ext.strip(".")}'))
        return [os.path.join(path, f) for f in pathes]
