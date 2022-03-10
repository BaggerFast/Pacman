import os
from typing import List


class PathManager:
    ROOT_DIR = os.path.dirname(os.path.abspath('run.py'))

    @classmethod
    def get_path(cls, path) -> str:
        return os.path.join(*[cls.ROOT_DIR] + path.lower().replace('\\', '/').split('/'))

    @classmethod
    def get_image_path(cls, path) -> str:
        return cls.get_path(f'assets/images/{path}')

    @classmethod
    def get_list_path(cls, path: str, ext: str) -> List[str]:
        path = cls.get_path(path)
        pathes = [f for f in os.listdir(path) if f.endswith(f'.{ext.strip(".")}')]
        pathes.sort(key=lambda x: x.split(f'.{ext.strip(".")}'))
        return [os.path.join(*[path, f]) for f in pathes]
