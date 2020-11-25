import os
from typing import List

from misc.constants import ROOT_DIR


def get_image_path(filename, *folder):
    """
    :param filename: имя файла с расширением или без
    :param folder: указать папки через пробел слева на право без image
    :return: возращает полный путь файла строкой
    """
    extension = '.png'
    if extension not in filename:
        filename += extension
    return os.path.join(*[ROOT_DIR, 'images'] + list(folder) + [filename])

def get_sound_path(filename, *folder):
    """
    :param filename: имя файла с расширением или без
    :param folder: указать папки через пробел слева на право без image
    :return: возращает полный путь файла строкой
    """
    extension = '.wav'
    if extension not in filename:
        filename += extension
    return os.path.join(*[ROOT_DIR, 'sounds'] + list(folder) + [filename])


def get_files_count(path):
    count = 0
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            count += 1
    return count


def get_image_path_for_animator(*folder: List[str]) -> List[str]:
    """
    :param folder: указать папки через пробел слева на право без имени файла без image
    :return: возращает все файлы для анимации автоматически
    """
    extension = '.png'
    images = []
    folder_path = [ROOT_DIR, 'images'] + list(folder)
    frames_count = get_files_count(os.path.join(*folder_path))
    for i in range(frames_count):
        images.append(os.path.join(*folder_path + [str(i) + extension]))
    return images


def create_file_if_not_exist(filepath: str, data=""):
    """
    :param filepath: path to file
    :param data: string which will written in file if it doesn't exist
    """
    if not os.path.exists(filepath):
        file = open(filepath, 'w')
        file.write(data)
        file.close()
