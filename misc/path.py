import os
from typing import List
from config.settings import Dir


class PathManager:

    @staticmethod
    def get_path(path: str) -> str:
        return os.path.join(Dir.BASE, path)

    @classmethod
    def get_asset_path(cls, path) -> str:
        return os.path.join(Dir.ASSET, path)

    @classmethod
    def get_image_path(cls, path) -> str:
        return os.path.join(Dir.IMAGE, path)

    @classmethod
    def get_list_path(cls, path: str, ext: str) -> List[str]:
        path = cls.get_path(path)
        pathes = [f for f in os.listdir(path) if f.endswith(f'.{ext.strip(".")}')]
        pathes.sort(key=lambda x: x.split(f'.{ext.strip(".")}'))
        return [os.path.join(path, f) for f in pathes]
