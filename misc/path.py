import os
from typing import List
import pygame as pg

ROOT_DIR = os.path.dirname(os.path.abspath('run.py'))


def get_path(path) -> str:
    return os.path.join(*[ROOT_DIR] + path.lower().replace('\\', '/').split('/'))


def get_list_path(path, ext) -> List[str]:
    """
    :param folder: указать папки через пробел слева на право без имени файла без image
    :param extension: указать расширение файла
    :return: возращает все пути до файлов для анимации автоматически
    """
    path = get_path(path)
    pathes = [f for f in os.listdir(path) if f.endswith(f'.{ext.strip(".")}')]
    pathes = sorted(pathes, key=lambda x: int(
        x.split(f'.{ext.strip(".")}')[0] if x.split(f'.{ext.strip(".")}')[0].isdigit() else x))

    return [os.path.join(*[path, f]) for f in pathes if f.endswith(f'.{ext.strip(".")}')]


def create_file_if_not_exist(filepath: str, data: str = "") -> None:
    """
    :param filepath: path to file
    :param data: string which will written in file if it doesn't exist
    """
    if not os.path.exists(filepath):
        file = open(filepath, 'w')
        file.write(data)
        file.close()

#
# def check_collision(rect1: pg.Rect, rect2: pg.Rect):
#     return rect1.center == rect2.center
